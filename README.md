# worldcup-predictor-live-skill

`worldcup-predictor-live-skill` 是一个用于 2026 世界杯赛前分析的 Codex Skill。它不是“猜比分脚本”，而是一套可复盘的预测工作流：每天先刷新已完赛数据，复盘上一天预测，再用最新样本、双方本届表现、晋级动机和多因子公式去分析下一比赛日。

> 说明：本项目只用于足球分析与研究，不提供投注、下注或赔率套利建议。精确比分是高方差事件，Skill 会记录 Top1 / Top3 / Top5 覆盖率，而不是承诺单一比分长期高命中。

## 它能做什么

- 从 ESPN public API 刷新世界杯已完赛记录。
- 生成本届实时概率基线：
  - 全场比分分布
  - 半全场 9 格分布
  - 总进球数分布
  - 平局率、双方进球率、3 球以上概率等聚合信号
- 逐场提取双方本届已完赛轨迹：
  - 半场/全场比分
  - 进球、失球、净胜球
  - 零封、被零封、双方进球
  - 防线崩盘、低比分控制、进攻趋势
- 分析第三轮和出线相关动机：
  - 稳晋级是否降速
  - 是否争头名/净胜球
  - 是否可能为了避强队而控节奏
  - 必须赢或将被淘汰的一方是否后程发力
- 引入多因子公式校准：
  - FIFA 积分差
  - FIFA 排名差
  - 球队状态
  - 教练能力
  - 近 20 年战绩
  - 足球强洲因素
  - 比赛环境/地理位置
  - 黑马/爆冷指数
- 输出每场比赛的：
  - 胜平负概率
  - 首选比分
  - Top3 / Top5 精确比分候选
  - 置信度
  - 最大变量
  - 复盘口径

## 方法框架

Skill 的预测顺序是：

1. 确认目标比赛开球时间，避免使用开球之后的数据。
2. 刷新并读取目标开球前已完赛样本。
3. 读取双方本届已完赛轨迹。
4. 判断积分压力、晋级路径和对手选择动机。
5. 结合阵容、伤停、停赛、战术对位和天气/场地。
6. 用多因子公式生成胜平负先验。
7. 用本届实时概率基线校准比分、半全场和总进球。
8. 生成 Top5 精确比分候选矩阵。
9. 每天复盘上一日预测，把失败案例写回参考文件。

多因子公式只是校准层，不能覆盖实时赛果轨迹和赛前情报。如果公式和本届实际走势冲突，以本届轨迹、阵容情报和晋级动机为主。

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

每日循环建议按这个顺序执行：

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

## 重要文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | Codex Skill 主说明，定义完整预测流程和输出格式。 |
| `scripts/update_worldcup_snapshot.py` | 从 ESPN public API 拉取赛果并计算概率分布。 |
| `data/completed_matches_seed.csv` | 英文版已完赛记录。 |
| `data/completed_matches_seed_zh.csv` | 中文字段和中文队名版本。 |
| `data/probability_snapshot_seed.json` | 机器可读概率快照。 |
| `references/live_probability_reference_seed.md` | 人类可读的本届概率基线。 |
| `references/prediction_audit_seed.md` | 预测前后对比与失败复盘。 |
| `references/exact_score_calibration_seed.md` | 精确比分 Top1/Top3/Top5 校准规则。 |
| `references/multi_factor_formula_seed.md` | 多因子公式、权重和使用边界。 |
| `templates/manual_match_row.csv` | ESPN 不可用时的手动补录模板。 |

## 输出示例

单场输出会包含这些部分：

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
