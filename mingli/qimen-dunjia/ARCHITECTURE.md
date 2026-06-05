# 奇门遁甲系统架构

## 三层架构

```
Layer 1: 排盘引擎    qimen.py + data/*.json (13) + verify.py (144项自检)
Layer 2: 断卦SOP     ~/.claude/skills/qimen-duanjua/skill.md (9步)
Layer 3: 独立复核    ~/.claude/agents/qimen-evaluator.md (GAN模式)
```

## 数据流

```
用户输入(时间+问题)
  ↓
qimen.paipan() → 9步排盘 → output.json
  ↓
verify.verify_one() → 144项断言自检 → 失败则按决策树修复
  ↓
加载 data/duanjua_knowledge.json（所有解读查表，不靠模型记忆）
  ↓
9步断卦SOP（盘外→用神→格局→大环境→值符值使→竖看→横看→综合→应期）
  ↓
qimen-evaluator 独立复核（从JSON独立推导，找矛盾）
  ↓
输出报告 + 记录 traces/ + 追加 Obsidian 日记
```

## 文件清单

| 文件 | 用途 |
|------|------|
| `qimen.py` | 排盘引擎（9步：四柱→节气→定局→地盘→旬首→值符值使→天盘→人盘→神盘） |
| `verify.py` | 自检脚本（144项断言，格式层+逻辑层+一致性） |
| `output.json` | 排盘输出（evaluator 读此文件） |
| `traces/` | 断卦 trace 日志（结构化JSON，用于迭代分析） |
| `analyze_traces.py` | 失败模式分析脚本 |
| `ARCHITECTURE.md` | 本文件 |
| `KNOWN_ISSUES.md` | 已知坑和防线 |
| `SKILL.md` | → 断卦SOP Skill（符号链接） |
| `EVALUATOR.md` | → 独立复核 Agent（符号链接） |

### data/ 数据文件

| 文件 | 用途 |
|------|------|
| `yuandan.json` | 九宫原始信息（星/门/神原宫、排列顺序） |
| `dipan_18ju.json` | 阴阳遁18局地盘排布 |
| `jieqi_jushu.json` | 24节气对应局数 |
| `shigan_keying_81.json` | 81组十干克应格局 |
| `duanjua_knowledge.json` | 断卦知识库（用神表/八神八门九星吉凶/五行生克/横看/应期） |
| `wuxing.json` | 五行生克+月令旺衰 |
| `kongwang.json` | 旬空表 |
| `jixing.json` | 击刑表 |
| `rumu.json` | 入墓表 |
| `menpo.json` | 门迫/宫制表 |
| `masing.json` | 马星表 |
| `wubuyushi.json` | 五不遇时表 |
| `futou.json` | 符头+地支分类（上中下元） |
| `dizhi_gong.json` | 地支对宫表 |

## 关键依赖

- `sxtwl` — 四柱计算唯一可靠来源（手算必错）
- 格局名必须查 `shigan_keying_81.json`（模型记忆必错，之前3个名字全错）
- 门迫必须程序自动扫描（人眼必漏，之前漏4处）

## 防线

1. **pre-commit hook** — 每次提交自动跑50盘随机验证，不过不让提交
2. **verify.py 144项断言** — 格式层（干支合法性）+ 逻辑层（偏移一致性）+ 一致性层（伏吟反吟独立重算）
3. **断卦知识库查表** — 所有吉凶/格局/生克解读从JSON查，不靠模型记忆
4. **evaluator 独立复核** — Sonnet模型从盘面JSON独立推导，找出解读与数据的矛盾
5. **trace 日志** — 每次断卦记录结构化JSON，用于批量分析失败模式和迭代改进

## 排盘9步

1. 四柱（sxtwl库）
2. 节气+阴阳遁（精确交节时刻）
3. 拆补法定局（符头→元→局数）
4. 地盘排布（查dipan_18ju）
5. 旬首+六仪+空亡
6. 值符星+值使门
7. 天盘九星+天干（值符星随时干转）
8. 人盘八门（值使门随时干步数转）
9. 神盘八神（阳顺阴逆）

## 断卦9步SOP

0. 盘外梳理（复述问题、确定聚焦）
1. 确定用神（查用神对照表）
2. 盘外格局（五不遇时、日时干关系）
3. 大环境（月令旺衰、伏吟反吟、内外盘）
4. 值符值使（天时走向+结局指向）
5. 竖看五层（干/星/门/神/格局 + 四害检查）
6. 横看（用神间落宫五行生克）
7. 综合判断（吉凶汇总+结论）
8. 定应期（空亡>马星>墓库>生旺>值使门）
