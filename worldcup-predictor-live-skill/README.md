# worldcup-predictor-live-skill

实时赛果概率增强版世界杯预测 skill。

## 目录

- `SKILL.md`：主 skill。
- `scripts/update_worldcup_snapshot.py`：抓取 ESPN 赛果并计算概率分布。
- `data/`：生成的完赛赛果和概率快照。
- `references/live_probability_reference_seed.md`：当前种子快照的人类可读版。
- `references/prediction_audit_seed.md`：旧版预测前后对比与复盘模板。
- `references/exact_score_calibration_seed.md`：精确比分 Top1/Top3/Top5 校准规则。
- `references/multi_factor_formula_seed.md`：从用户提供图片整理出的多因子权重和公式。
- `templates/manual_match_row.csv`：数据源不可用时的手动补录模板。

## 当前硬性要求

每场预测前必须从 `data/completed_matches_seed.csv` 提取双方在目标开球前的本届已完赛轨迹，包括比分、半场、半全场、进失球、零封/被零封、双方进球和比赛状态，再判断晋级路径、避强队可能性、稳晋级降速或淘汰边缘发力因素，最后进入胜平负概率与精确比分候选矩阵。

每场还必须增加一层多因子公式校准：FIFA积分差、FIFA排名差、球队状态、教练能力、近20年战绩、足球强洲、比赛环境和黑马/爆冷指数。该层只作启发式校准，不覆盖实时赛果和赛前情报。

## 快速更新

```bash
python scripts/update_worldcup_snapshot.py --dates 20260611-20260621 --out-dir data
```

预测某场前，推荐加上目标场次开球时间：

```bash
python scripts/update_worldcup_snapshot.py --dates 20260611-20260621 --target-kickoff-utc "2026-06-21T19:00:00Z" --out-dir data
```
