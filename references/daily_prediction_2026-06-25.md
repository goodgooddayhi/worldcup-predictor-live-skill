# 2026-06-25 每日复盘与预测

生成时间：2026-06-25 02:40 左右，北京时间  
预测范围：北京时间 2026-06-25 的全部 6 场世界杯小组赛  
数据源：ESPN public API 快照 + RotoWire 赛前情报 + 天气查询

## 一、上一比赛日复盘

来自对话 `019ee97f-423c-79f2-96bd-abedb3aaf584` 的 2026-06-24 北京时间 4 场预测：

| 比赛 | 预测 | 实际 | 方向 | 比分 |
|------|------|------|------|------|
| 葡萄牙 vs 乌兹别克斯坦 | 葡萄牙 3-1 | 葡萄牙 5-0 | 对 | 错 |
| 英格兰 vs 加纳 | 英格兰 3-0 | 0-0 | 错 | 错 |
| 巴拿马 vs 克罗地亚 | 克罗地亚 2-1 | 克罗地亚 1-0 | 对 | 错 |
| 哥伦比亚 vs 刚果金 | 哥伦比亚 2-1 | 哥伦比亚 1-0 | 对 | 错 |

结论：方向 3/4，精确比分 0/4。最大修正是：强队反弹局要给大胜备选，但头名战或双方都有分的比赛，平局必须进入核心候选；低位队连续验证后，热门小胜应优先考虑 1-0/2-0，而不是机械给双方进球。

复盘已追加到 `references/prediction_audit_seed.md`。

## 二、本次概率基线

- 赛果统计截止：2026-06-24 18:38 UTC 左右
- 已纳入完赛样本：48 场
- 高频比分：1-1 14.58%；0-0、0-1、1-0、2-0 各 8.33%；2-2、3-0 各 6.25%
- 半全场Top：胜胜 33.33%；平胜 16.67%；平平 16.67%；负负 12.50%
- 总进球Top：2球 22.92%；4球 18.75%；1球 16.67%；3球 12.50%；5球 10.42%
- 场均总进球：2.94
- 平局率：29.17%

说明：本次统一在 03:00 首场开球前完成预测，后续 06:00、09:00 场次若临近开球前已有新增完赛，应再刷新一次快照滚动修正。

## 三、2026-06-25 赛程与预测

### 1. 瑞士 vs 加拿大

- 北京时间：2026-06-25 03:00
- UTC：2026-06-24 19:00
- 场地：BC Place, Vancouver
- 类型：C 头名战
- 积分压力：双方同为 4 分，平局大概率都能晋级，主要争小组第一。
- 关键情报：加拿大 Kone 和 Alfie Jones 缺席，Eustaquio 存疑但预计首发；瑞士 Muheim 存疑但不在预计首发。瑞士依赖 Xhaka 控节奏和 Akanji 防线，加拿大靠 David/Larin 双前锋和主场压迫。
- 战术判断：这场最容易被“主场气势”带高预期，但复盘后应把平局放在核心。瑞士能控住节奏，加拿大会抢开局；双方都不需要冒险把结构打散。
- 胜平负概率：瑞士胜 34% / 平 35% / 加拿大胜 31%
- 比分预测：首选 1-1；备选 0-0、1-0 瑞士
- 半全场倾向：平平 > 平胜
- 置信度：中
- 最大变量：Eustaquio 是否能健康首发并承受瑞士中场压迫。

### 2. 波黑 vs 卡塔尔

- 北京时间：2026-06-25 03:00
- UTC：2026-06-24 19:00
- 场地：Lumen Field, Seattle
- 类型：A 生死战
- 积分压力：两队均 1 分，输球出局，赢球保留出线希望。
- 关键情报：卡塔尔 Homam Ahmed 与 Assim Madibo 停赛，Afif 仍是主要创造点；波黑更依赖 Dzeko、Demirovic 的禁区支点和定位球。
- 战术判断：两队都必须赢，但卡塔尔防守和纪律性问题更明显。波黑若能把球送到 Dzeko 周围，会在二点和定位球上有优势；风险是压上后被 Afif 转换。
- 胜平负概率：波黑胜 55% / 平 22% / 卡塔尔胜 23%
- 比分预测：首选 2-1 波黑；备选 1-0 波黑、1-1
- 半全场倾向：平胜 > 胜胜
- 置信度：中
- 最大变量：卡塔尔能否让 Afif 在反击中直接制造进球。

### 3. 苏格兰 vs 巴西

- 北京时间：2026-06-25 06:00
- UTC：2026-06-24 22:00
- 场地：Hard Rock Stadium, Miami
- 类型：B 不对等压力战
- 积分压力：苏格兰 3 分但必须击败巴西才稳，巴西 4 分基本占优并争头名。
- 关键情报：巴西 Raphinha 缺席，Neymar 存疑；预计仍有 Vinicius Junior、Matheus Cunha、Lucas Paqueta、Rayan。苏格兰需要 McTominay、McGinn、Robertson 推动进攻。
- 天气与节奏：迈阿密有雷暴风险，可能降低连续压制质量，也可能造成比赛碎片化。
- 战术判断：苏格兰必须主动，反而会给巴西反击空间。巴西不是完全顺，但个人能力和转换速度仍高一档；Raphinha 缺席使大胜上限略降。
- 胜平负概率：苏格兰胜 21% / 平 25% / 巴西胜 54%
- 比分预测：首选 1-2 巴西；备选 0-2 巴西、1-1
- 半全场倾向：平胜 > 胜胜
- 置信度：中偏低
- 最大变量：雷暴/中断与苏格兰首球；若苏格兰先进球，巴西胜率会明显下降。

### 4. 摩洛哥 vs 海地

- 北京时间：2026-06-25 06:00
- UTC：2026-06-24 22:00
- 场地：Mercedes-Benz Stadium, Atlanta
- 类型：D 功能性大胜场
- 积分压力：摩洛哥 4 分仍要争头名和净胜球；海地 0 分已出局。
- 关键情报：海地暂无主要伤病，预计更开放地使用双前锋；摩洛哥有 Hakimi、Brahim Diaz、Ounahi 等多点推进。
- 战术判断：海地放开踢会增加进球娱乐性，但也会给摩洛哥边路和肋部空间。复盘后的规则支持：强队有净胜球动机 + 对手已出局且防守不稳时，大胜备选必须进入。
- 胜平负概率：摩洛哥胜 70% / 平 18% / 海地胜 12%
- 比分预测：首选 3-0 摩洛哥；备选 2-0 摩洛哥、3-1 摩洛哥
- 半全场倾向：胜胜 > 平胜
- 置信度：中高
- 最大变量：摩洛哥是否提前轮换；若明显保守，比分会退回 2-0。

### 5. 南非 vs 韩国

- 北京时间：2026-06-25 09:00
- UTC：2026-06-25 01:00
- 场地：Estadio BBVA, Monterrey
- 类型：B 不对等压力战
- 积分压力：韩国 3 分，平局大概率够用；南非 1 分必须赢并看另一场结果。
- 关键情报：南非 Mokoena 和 Themba Zwane 停赛，中场损失很重；韩国无主要伤病，Son、Lee Kang-in、Kim Min-jae 架构完整。
- 战术判断：南非不得不更主动，但中场缺两名关键球员会削弱控球与定位球质量。韩国可以等转换，Son 和 Lee Kang-in 的反击质量更适合惩罚后场空间。
- 胜平负概率：南非胜 24% / 平 27% / 韩国胜 49%
- 比分预测：首选 1-2 韩国；备选 1-1、0-1 韩国
- 半全场倾向：平胜 > 平平
- 置信度：中
- 最大变量：韩国是否满足于平局；如果他们过早降速，1-1 会抬升为首选。

### 6. 捷克 vs 墨西哥

- 北京时间：2026-06-25 09:00
- UTC：2026-06-25 01:00
- 场地：Estadio Banorte
- 类型：B 不对等压力战
- 积分压力：墨西哥 6 分已出线，捷克 1 分必须赢才有希望。
- 关键情报：墨西哥暂无主要伤病，预计仍可能接近主力；捷克 David Jurasek 肌肉伤基本缺席。捷克要主动压上，墨西哥可控节奏。
- 战术判断：这是最容易出现“强队不急、弱队必须冲”的场。墨西哥质量更高，但出线已定会让比赛管理优先级上升；捷克的进攻压力会创造机会，也会留下反击空间。
- 胜平负概率：捷克胜 22% / 平 35% / 墨西哥胜 43%
- 比分预测：首选 1-1；备选 1-2 墨西哥、0-1 墨西哥
- 半全场倾向：平平 > 平负
- 置信度：中
- 最大变量：墨西哥轮换幅度；若确认大轮换，平局权重继续上调。

## 四、汇总

| 比赛 | 首选比分 | 倾向 | 风险 |
|------|----------|------|------|
| 瑞士 vs 加拿大 | 1-1 | 平局 | 加拿大主场压迫打出早球 |
| 波黑 vs 卡塔尔 | 2-1 | 波黑小胜 | Afif 反击爆点 |
| 苏格兰 vs 巴西 | 1-2 | 巴西小胜 | 雷暴/苏格兰先进球 |
| 摩洛哥 vs 海地 | 3-0 | 摩洛哥胜 | 摩洛哥轮换降速 |
| 南非 vs 韩国 | 1-2 | 韩国小胜 | 韩国满足平局 |
| 捷克 vs 墨西哥 | 1-1 | 平局优先 | 墨西哥近主力反击打穿 |

最稳方向：摩洛哥胜、韩国不败。  
最容易出平：瑞士 vs 加拿大、捷克 vs 墨西哥。  
最容易偏离比分：苏格兰 vs 巴西，因为天气、苏格兰生死战和巴西伤病变量叠在一起。

## 五、来源

- ESPN public API: https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard
- RotoWire Switzerland vs Canada: https://www.rotowire.com/soccer/article/switzerland-vs-canada-preview-predicted-lineups-team-news-tactical-analysis-2026-world-cup-group-b-119339
- RotoWire Bosnia and Herzegovina vs Qatar: https://www.rotowire.com/soccer/article/bosnia-and-herzegovina-vs-qatar-preview-predicted-lineups-team-news-tactical-analysis-2026-world-cup-group-b-119338
- RotoWire Scotland vs Brazil: https://www.rotowire.com/soccer/article/scotland-vs-brazil-preview-predicted-lineups-team-news-tactical-analysis-2026-world-cup-group-c-119341
- RotoWire Morocco vs Haiti: https://www.rotowire.com/soccer/article/morocco-vs-haiti-preview-predicted-lineups-team-news-tactical-analysis-2026-world-cup-group-c-119340
- RotoWire South Africa vs South Korea: https://www.rotowire.com/soccer/article/south-africa-vs-south-korea-preview-predicted-lineups-team-news-tactical-analysis-2026-world-cup-group-a-119344
- RotoWire Czechia vs Mexico: https://www.rotowire.com/soccer/article/czechia-vs-mexico-preview-predicted-lineups-team-news-tactical-analysis-2026-world-cup-group-a-119342
