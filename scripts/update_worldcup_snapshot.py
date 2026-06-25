#!/usr/bin/env python3
"""Refresh 2026 World Cup result probability snapshots from ESPN public APIs.

The snapshot is intentionally simple and auditable:
- completed_matches_seed.csv: one row per completed match
- probability_snapshot_seed.json: scoreline, HT/FT, and total-goals distributions

Use --target-kickoff-utc when predicting a future match so the model only sees
matches completed before that kickoff, avoiding data leakage.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


ESPN_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"
ESPN_SUMMARY = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary?event={event_id}"


def fetch_json(url: str, retries: int = 3) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "worldcup-predictor-skill/1.0"})
            with urlopen(req, timeout=25) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001 - report exact fetch failure to user.
            last_error = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def result_symbol(goals_for: int, goals_against: int) -> str:
    if goals_for > goals_against:
        return "胜"
    if goals_for == goals_against:
        return "平"
    return "负"


def pct(count: int, total: int) -> float:
    return round(count * 100 / total, 2) if total else 0.0


def parse_halftime_from_text(text: str, home: str, away: str) -> tuple[int, int] | None:
    # Example: "First Half ends, Mexico 1, South Africa 0."
    pattern = rf"First Half ends,\s*{re.escape(home)}\s+(\d+),\s*{re.escape(away)}\s+(\d+)"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None


def extract_match(event: dict[str, Any], include_halftime: bool) -> dict[str, Any] | None:
    comp = event["competitions"][0]
    status = comp["status"]["type"]
    if not status.get("completed"):
        return None

    competitors = comp["competitors"]
    home = next(c for c in competitors if c["homeAway"] == "home")
    away = next(c for c in competitors if c["homeAway"] == "away")
    home_team = home["team"]["displayName"]
    away_team = away["team"]["displayName"]
    home_abbr = home["team"].get("abbreviation", "")
    away_abbr = away["team"].get("abbreviation", "")
    home_goals = int(home["score"])
    away_goals = int(away["score"])

    row: dict[str, Any] = {
        "event_id": event["id"],
        "date_utc": event["date"],
        "stage": event.get("season", {}).get("slug", "group-stage"),
        "group": comp.get("notes", [{}])[0].get("headline", "") if comp.get("notes") else "",
        "venue": comp.get("venue", {}).get("fullName", ""),
        "home_team": home_team,
        "away_team": away_team,
        "home_abbr": home_abbr,
        "away_abbr": away_abbr,
        "home_goals": home_goals,
        "away_goals": away_goals,
        "scoreline_home": f"{home_goals}-{away_goals}",
        "total_goals": home_goals + away_goals,
        "full_result_home": result_symbol(home_goals, away_goals),
        "source": "ESPN public API",
    }

    if not include_halftime:
        row.update(
            {
                "ht_home_goals": "",
                "ht_away_goals": "",
                "halftime_score_home": "",
                "halftime_result_home": "",
                "ht_ft_home": "",
            }
        )
        return row

    summary = fetch_json(ESPN_SUMMARY.format(event_id=event["id"]))
    ht_home = 0
    ht_away = 0
    found_from_events = False

    for key_event in summary.get("keyEvents", []):
        if key_event.get("type", {}).get("type") == "halftime":
            parsed = parse_halftime_from_text(key_event.get("text", ""), home_team, away_team)
            if parsed:
                ht_home, ht_away = parsed
                found_from_events = True
                break

    if not found_from_events:
        for key_event in summary.get("keyEvents", []):
            if not key_event.get("scoringPlay"):
                continue
            if key_event.get("period", {}).get("number") != 1:
                continue
            scoring_team = key_event.get("team", {}).get("displayName")
            if scoring_team == home_team:
                ht_home += 1
            elif scoring_team == away_team:
                ht_away += 1

    ht_result = result_symbol(ht_home, ht_away)
    ft_result = result_symbol(home_goals, away_goals)
    row.update(
        {
            "ht_home_goals": ht_home,
            "ht_away_goals": ht_away,
            "halftime_score_home": f"{ht_home}-{ht_away}",
            "halftime_result_home": ht_result,
            "ht_ft_home": f"{ht_result}{ft_result}",
        }
    )
    return row


def build_snapshot(matches: list[dict[str, Any]], generated_at: str, args: argparse.Namespace) -> dict[str, Any]:
    total = len(matches)
    scorelines = Counter(m["scoreline_home"] for m in matches)
    ht_ft = Counter(m["ht_ft_home"] for m in matches if m.get("ht_ft_home"))
    total_goals = Counter(str(m["total_goals"]) for m in matches)

    ht_ft_order = ["胜胜", "胜平", "胜负", "平胜", "平平", "平负", "负胜", "负平", "负负"]

    return {
        "generated_at_utc": generated_at,
        "source": {
            "name": "ESPN public API",
            "scoreboard_url": ESPN_SCOREBOARD,
            "date_range": args.dates,
            "target_kickoff_utc": args.target_kickoff_utc,
        },
        "completed_match_count": total,
        "included_boundary_rule": "Only completed matches are included; if target_kickoff_utc is set, matches at or after that kickoff are excluded.",
        "scoreline_distribution_home_perspective": [
            {"scoreline": key, "count": count, "probability_pct": pct(count, total)}
            for key, count in sorted(scorelines.items(), key=lambda item: (-item[1], item[0]))
        ],
        "ht_ft_distribution_home_perspective": [
            {"result": key, "count": ht_ft.get(key, 0), "probability_pct": pct(ht_ft.get(key, 0), total)}
            for key in ht_ft_order
        ],
        "total_goals_distribution": [
            {"total_goals": int(key), "count": count, "probability_pct": pct(count, total)}
            for key, count in sorted(total_goals.items(), key=lambda item: (int(item[0]), item[1]))
        ],
        "aggregate": {
            "avg_total_goals": round(sum(m["total_goals"] for m in matches) / total, 3) if total else 0,
            "draw_count": sum(1 for m in matches if m["home_goals"] == m["away_goals"]),
            "draw_probability_pct": pct(sum(1 for m in matches if m["home_goals"] == m["away_goals"]), total),
            "over_2_5_count": sum(1 for m in matches if m["total_goals"] >= 3),
            "over_2_5_probability_pct": pct(sum(1 for m in matches if m["total_goals"] >= 3), total),
            "both_teams_scored_count": sum(1 for m in matches if m["home_goals"] > 0 and m["away_goals"] > 0),
            "both_teams_scored_probability_pct": pct(
                sum(1 for m in matches if m["home_goals"] > 0 and m["away_goals"] > 0), total
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dates", default="20260611-20260621", help="ESPN date range, e.g. 20260611-20260621")
    parser.add_argument("--target-kickoff-utc", default="", help="Optional ISO UTC kickoff; excludes matches at/after it")
    parser.add_argument("--out-dir", default="../data", help="Output directory")
    parser.add_argument("--skip-halftime", action="store_true", help="Skip summary calls and omit HT/FT stats")
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    target_kickoff = parse_utc(args.target_kickoff_utc)
    data = fetch_json(f"{ESPN_SCOREBOARD}?dates={args.dates}&limit=120")

    matches: list[dict[str, Any]] = []
    for event in data.get("events", []):
        event_time = parse_utc(event.get("date"))
        if target_kickoff and event_time and event_time >= target_kickoff:
            continue
        row = extract_match(event, include_halftime=not args.skip_halftime)
        if row:
            matches.append(row)

    matches.sort(key=lambda m: (m["date_utc"], m["event_id"]))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "completed_matches_seed.csv"
    json_path = out_dir / "probability_snapshot_seed.json"

    fieldnames = [
        "event_id",
        "date_utc",
        "stage",
        "group",
        "venue",
        "home_team",
        "away_team",
        "home_abbr",
        "away_abbr",
        "home_goals",
        "away_goals",
        "scoreline_home",
        "total_goals",
        "ht_home_goals",
        "ht_away_goals",
        "halftime_score_home",
        "halftime_result_home",
        "full_result_home",
        "ht_ft_home",
        "source",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matches)

    snapshot = build_snapshot(matches, generated_at, args)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"completed_matches={len(matches)}")
    print(f"csv={csv_path}")
    print(f"json={json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
