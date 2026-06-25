# WorldCup Predictor Live Skill

一个面向 2026 世界杯的实时赛果概率增强预测 Skill。

它不是简单地“猜比分”，而是一套可复盘的足球赛前分析流程：每天刷新已完赛数据，复盘上一天预测，再结合本届实时样本、双方完赛轨迹、晋级动机、多因子公式和赛前情报，分析下一比赛日的全部场次。

[![Skill](https://img.shields.io/badge/Skill-WorldCup%20Predictor-blue)](./SKILL.md)
[![Data](https://img.shields.io/badge/Data-ESPN%20Snapshot-green)](./data/probability_snapshot_seed.json)
[![Language](https://img.shields.io/badge/Language-中文-orange)](./README.md)

> 本项目只用于足球分析与研究，不提供投注、下注或赔率套利建议。精确比分是高方差事件，Skill 会记录 Top1 / Top3 / Top5 覆盖率，而不是承诺单一比分长期高命中。

## 一句话安装

把下面这句话发给你的 Agent：

```text
帮我安装这个 skill：https://github.com/goodgooddayhi/worldcup-predictor-live-skill
```

适用于 Codex、Claude Code、Cursor、Roo Code、Cline、Trae、Windsurf 等支持读取仓库/本地 Skill 指令的 Agent。不同 Agent 的安装目录不同，但都可以让 Agent 根据仓库里的 `SKILL.md` 和 `README.md` 自动完成安装。

## 手动安装

### 1. 克隆仓库

```bash
git clone https://github.com/goodgooddayhi/worldcup-predictor-live-skill.git
```

### 2. 放到你的 Agent Skill 目录

如果你的 Agent 有固定的 skills 目录，把整个仓库目录放进去即可。例如：

```text
skills/
└── worldcup-predictor-live-skill/
    ├── SKILL.md
    ├── data/
    ├── references/
    ├── scripts/
    └── templates/
```

### 3. 让 Agent 读取 `SKILL.md`

安装后可以直接对 Agent 说：

```text
使用 worldcup-predictor-live-skill，复盘上一天比赛并预测下一天全部世界杯场次。
```

## 适合谁用

| 使用者 | 用法 |
|--------|------|
| Codex / Claude Code 用户 | 作为 Skill 安装，让 Agent 每天自动复盘和预测。 |
| 数据分析用户 | 使用 `data/` 和 `scripts/` 刷新赛果并计算概率基线。 |
| 足球内容创作者 | 生成可解释、可复盘的赛前分析稿。 |
| 自动化用户 | 接入 webhook，把每日预测报告推送到飞书、Slack、Discord 等。 |

## 核心能力

### 实时赛果概率

- 从 ESPN public API 刷新世界杯已完赛记录。
- 计算全场比分分布。
- 计算半全场 9 格分布。
- 计算总进球数分布。
- 输出平局率、双方进球率、3 球以上概率等聚合信号。

### 双方本届轨迹

每场比赛都会先读取双方在本届世界杯中的已完赛表现：

- 半场/全场比分
- 进球、失球、净胜球
- 零封、被零封、双方进球
- 防线崩盘、低比分控制、进攻趋势
- 是否连续进球或连续被零封

### 晋级路径与比赛动机

第三轮和出线相关比赛会额外判断：

- 是否已经稳晋级
- 是否仍要争头名或净胜球
- 是否可能为了避开强队而控节奏
- 是否只需要平局
- 是否必须赢或即将被淘汰
- 已淘汰队是荣誉战放开踢，还是士气崩盘

### 多因子公式校准

Skill 会把用户提供的 12 张公式图整理成多因子校准层：

| 因素 | 权重 |
|------|------|
| FIFA 积分差 | 35% |
| FIFA 排名差 | 15% |
| 球队状态因素 | 15% |
| 教练能力 | 10% |
| 近 20 年战绩 | 10% |
| 足球强洲因素 | 5% |
| 比赛环境/地理位置 | 5% |
| 黑马/爆冷指数 | 5% |

多因子公式只是校准层，不覆盖实时赛果轨迹、阵容伤停和晋级动机。

## 预测流程

```text
刷新已完赛数据
  ↓
读取双方本届完赛轨迹
  ↓
判断积分压力与晋级路径
  ↓
分析阵容、伤停、战术、天气、场地
  ↓
计算多因子公式先验
  ↓
结合本届比分/半全场/总进球概率基线
  ↓
生成胜平负概率
  ↓
生成 Top5 精确比分候选矩阵
  ↓
赛后复盘并写回规则库
```

## 快速开始

刷新当前数据：

```bash
python scripts/update_worldcup_snapshot.py --dates 20260611-20260626 --out-dir data
```

预测某场前，建议指定目标开球时间，避免数据泄漏：

```bash
python scripts/update_worldcup_snapshot.py \
  --dates 20260611-20260626 \
  --target-kickoff-utc "2026-06-25T20:00:00Z" \
  --out-dir data
```

更新后会生成：

- `data/completed_matches_seed.csv`
- `data/probability_snapshot_seed.json`

## 每日自动化流程

1. 刷新 ESPN 已完赛数据。
2. 确认 `completed_match_count` 是否增加。
3. 复盘上一比赛日：
   - 方向命中
   - Top1 精确比分
   - Top3 覆盖
   - Top5 覆盖
   - 误差距离
4. 把复盘追加到 `references/prediction_audit_seed.md`。
5. 如果比分偏差明显，更新 `references/exact_score_calibration_seed.md`。
6. 预测下一比赛日所有场次。
7. 输出日报或推送到外部 webhook。

## 文件结构

```text
.
├── SKILL.md
├── README.md
├── data/
│   ├── completed_matches_seed.csv
│   ├── completed_matches_seed_zh.csv
│   └── probability_snapshot_seed.json
├── references/
│   ├── daily_prediction_2026-06-25.md
│   ├── daily_prediction_2026-06-26.md
│   ├── exact_score_calibration_seed.md
│   ├── live_probability_reference_seed.md
│   ├── multi_factor_formula_seed.md
│   └── prediction_audit_seed.md
├── scripts/
│   └── update_worldcup_snapshot.py
└── templates/
    └── manual_match_row.csv
```

## 重要文件

| 文件 | 作用 |
|------|------|
| `SKILL.md` | Skill 主说明，定义完整预测流程和输出格式。 |
| `scripts/update_worldcup_snapshot.py` | 从 ESPN public API 拉取赛果并计算概率分布。 |
| `data/completed_matches_seed.csv` | 英文版已完赛记录。 |
| `data/completed_matches_seed_zh.csv` | 中文字段和中文队名版本。 |
| `data/probability_snapshot_seed.json` | 机器可读概率快照。 |
| `references/live_probability_reference_seed.md` | 人类可读的本届概率基线。 |
| `references/prediction_audit_seed.md` | 预测前后对比与失败复盘。 |
| `references/exact_score_calibration_seed.md` | 精确比分 Top1 / Top3 / Top5 校准规则。 |
| `references/multi_factor_formula_seed.md` | 多因子公式、权重和使用边界。 |
| `templates/manual_match_row.csv` | ESPN 不可用时的手动补录模板。 |

## 输出示例

```markdown
## 队A vs 队B 预测

### 数据边界
- 目标开球：YYYY-MM-DD HH:MM UTC
- 赛果统计截止：YYYY-MM-DD HH:MM UTC
- 已纳入完赛样本：N场

### 双方本届已完赛轨迹
- 队A：...
- 队B：...
- 轨迹结论：...

### 胜平负概率
队A胜 X% / 平 X% / 队B胜 X%

### 多因子公式校准
- FIFA积分差：...
- 排名差：...
- 球队状态：...
- 教练能力：...
- 近20年战绩：...
- 强洲/地理/黑马：...
- 多因子结论：...

### 比分预测
- 首选：X-X
- 备选：X-X、X-X
- 高风险候选：X-X、X-X

### 精确比分候选矩阵
| 排名 | 比分 | 候选权重 | 触发理由 |
|------|------|----------|----------|
| 1 | X-X | X% | ... |
| 2 | X-X | X% | ... |
| 3 | X-X | X% | ... |
| 4 | X-X | X% | ... |
| 5 | X-X | X% | ... |
```

## 当前数据快照

当前仓库内置快照包含 54 场已完赛记录，数据边界来自 ESPN public API。你可以随时重新运行更新脚本刷新数据。

## 数据源

主要数据源：

- ESPN public API scoreboard
- ESPN match summary API

辅助情报可来自：

- FIFA / 官方赛程
- RotoWire 赛前预览
- Sofascore FIFA rankings
- BBC、Guardian、Olympics.com 等公开报道

## 免责声明

这个 Skill 的目标是让预测过程可解释、可复盘、可迭代。它不会保证精确比分命中，也不应被用作投注或财务决策依据。
