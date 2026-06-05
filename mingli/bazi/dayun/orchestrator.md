# 八字大运流年 SOP 编排器（Orchestrator）

> 基于 11 份调研报告、250+ 条硬规则、1500+ 个量化数值
> 设计原则：查表驱动，每步有 Gate Check，消除 LLM 主观判断
> 对标：紫微斗数 Phase 5 harness 的机械化程度

---

## 设计原则

1. **查表不推理**：每个判断都有查表依据，LLM 不做主观评分
2. **Gate Check 门控**：每步输出必须通过结构化校验才能进入下一步
3. **Context Anxiety 防护**：后面的大运分析不得比前面粗糙
4. **卡片即接口**：每步输出卡片是下一步的唯一输入
5. **确定性标注**：每个结论标注来源规则编号，可追溯

---

## 前置条件

本 SOP 在 Phase 0-5 完成后执行（即命局排盘、旺衰判定、用神体系、格局判定、地支扫描、专项断事已完成）。

从前序 Phase 读取的必需数据：
```
Phase 0：四柱干支、藏干、十神、空亡、大运列表、神煞
Phase 1：五行统计、气候判定、地支关系
Phase 2：旺衰六级判定、格局名称、成败、调候满足度
Phase 3：用神/喜神/忌神/仇神/闲神、病药、十神组合
Phase 4：四柱逐柱关系（盖头截脚、天干合冲）
Phase 5：地支关系全扫描（合冲刑害空亡墓库暗合伏吟反吟）
```

---

## Step 路由表

| Step | 名称 | Harness 文件 | 推理强度 | 输出 | Gate Check |
|------|------|-------------|---------|------|-----------|
| 0 | 前序数据提取 | `dayun-step0-harness.md` | 🟢轻 | 前序数据卡 | 7 项前序数据完整 |
| 1 | 命局力量量化 | `dayun-step1-harness.md` | 🟢轻（查表填数） | 五行力量表 | 五行得分合计=总分 |
| 2 | 干支动态作用 | `dayun-step2-harness.md` | 🟡中（查表+判定） | 调整后力量表 | 合冲刑害全扫描 |
| 3 | 旺衰定级校验 | `dayun-step3-harness.md` | 🟢轻（查阈值） | 旺衰校验卡 | 量化结果与P2一致 |
| 4 | 格局调候校验 | `dayun-step4-harness.md` | 🟡中（查表+格局判定） | 格局调候校验卡 | 穷通宝鉴已查 |
| 5 | 原局信号扫描 | `dayun-step5-harness.md` | 🟡中（查信号表） | 原局信号清单 | 信号数>=1 |
| 6 | 逐步大运分析 | `dayun-step6-harness.md` | 🟡中（查表+叠加） | 大运逐步卡 | 步数>=6，每步>=9字段(a-i含伏吟反吟)，评分公式可复现 |
| 7 | 关键流年筛选 | `dayun-step7-harness.md` | 🟡中（9项规则扫描） | 关键流年表 | 关键流年>=5，分散>=3个大运，每年9项全查 |
| 8 | 断事信号匹配 | `dayun-step8-harness.md` | 🟡中（H01-H25+6类信号） | 事件预判卡 | 每关键流年H表25条全查+事件类型+信号强度 |
| 9 | 应期定位 | `dayun-step9-harness.md` | 🔴重（综合） | 应期卡 | 应期有流程依据 |
| 10 | 古籍交叉验证 | `dayun-step10-harness.md` | 🟢轻（查断语库） | 交叉验证卡 | 至少1条古籍印证 |
| 11 | 综合输出 | `dayun-step11-harness.md` | 🟡中（汇总） | 最终报告 | 校验清单全通过 |

---

## 执行流程

```
Phase 0-5 完成
    │
    ▼
┌─────────────────────────────────────────┐
│ Step N 执行循环                          │
│                                          │
│  1. Read(`dayun-stepN-harness.md`)       │
│  2. 读取前序卡片数据                      │
│  3. 按 harness 指令逐步执行（查表为主）    │
│  4. 输出本 Step 卡片                      │
│  5. Gate Check（机械校验）                │
│     ├── 通过 → 进入 Step N+1            │
│     └── 不通过 → 标注缺失项，补做后重检   │
│                                          │
│  ★ 推理强度按路由表调节                    │
│  ★ 所有评分必须有查表依据                  │
└─────────────────────────────────────────┘
    │
    ▼ (Step 11 完成)
    │
  最终输出：大运流年总卡 + 关键事件时间线
```

---

## Gate Check 规则汇总

### Step 0 Gate
```
ASSERT 四柱干支 != null（4组）
ASSERT 用神 != null
ASSERT 喜忌仇闲 != null（4个）
ASSERT 格局名称 != null
ASSERT 调候用神 != null
ASSERT 大运列表.length >= 6
ASSERT 地支关系扫描已完成
```
# 详见 harness 完整版
<!-- fix: P2-R1-2 Gate Check 同步注释 -->

### Step 1 Gate
```
ASSERT 五行得分表.count == 5（金木水火土各有分值）
ASSERT 五行得分.sum ∈ [500, 600]（合理范围校验）
ASSERT 日主得分 != null
```
# 详见 harness 完整版

### Step 2 Gate
```
ASSERT 天干合检查.pairs == 6（6对全查）
ASSERT 地支关系检查.done == true
ASSERT 调整后五行得分表 != null
```
# 详见 harness 完整版

### Step 3 Gate
<!-- fix: P1-R2-2 从格断言回写 orchestrator -->
```
ASSERT 旺衰等级 IN [旺极,太旺,偏旺,中和,偏弱,太弱,弱极,从格]
ASSERT 量化旺衰 与 Phase2定性旺衰 一致性标注
ASSERT 从格检查已执行（若日主得分<45或>450）
```
# 详见 harness 完整版

### Step 4 Gate
```
ASSERT 格局校验.done == true
ASSERT 调候查表.穷通宝鉴格 != null
ASSERT 调候满足度 IN [充分满足,部分满足,不满足]
```
# 详见 harness 完整版

### Step 5 Gate
```
ASSERT 原局信号.count >= 1
ASSERT 十神组合至少检查6项
```
# 详见 harness 完整版

### Step 6 Gate
```
ASSERT 大运分析.步数 >= 6
ASSERT 每步大运.字段数 >= 9（a-i全部判定项，含伏吟反吟检查）
ASSERT 每步大运.综合评分公式 != null（可复现，含判定i调整+判定c合绊调整）
ASSERT 每步大运.综合分 IN [0, 100]
ASSERT 每步大运.评级 IN [大吉, 吉, 小吉, 平, 小凶, 凶, 大凶]
ASSERT 后面的大运分析密度 >= 前面的（Context Anxiety 防护）
ASSERT 覆盖命主当前所在大运
```
# 详见 harness 完整版

### Step 7 Gate
```
ASSERT 关键流年.count >= 5
ASSERT 关键流年分散在 >= 3 个不同大运中
ASSERT 每个关键流年.命中规则数 >= 2
ASSERT 每个关键流年.规则编号列表 != null AND .length >= 2
ASSERT 每个关键流年.预判吉凶 IN [大吉, 吉, 小吉, 平, 小凶, 凶, 大凶]
ASSERT 所有流年.扫描完成 == true（无遗漏的大运或流年）
ASSERT 每个流年.九项检查(a-i) == done
ASSERT 关键流年汇总表.行数 >= 5
ASSERT 非关键流年.标注 IN ["平", "次关键"]
```
# 详见 harness 完整版

### Step 8 Gate
```
ASSERT 每个关键流年.H表检查数 == 25（H01-H25全部逐条）
ASSERT 每个关键流年.六类事件信号检查 == 6（M/P/F/D/L/S）
ASSERT 每个关键流年.事件类型 != null
ASSERT 每个关键流年.事件类型 IN [婚姻, 升职, 破财, 丧亲, 官非, 疾病, 综合, 不明确]
ASSERT 每个关键流年.信号强度 IN [强, 中, 弱]
ASSERT 每个关键流年.信号强度来源 已标注（H命中数+事件信号命中数）
ASSERT 每个关键流年.确定性标注 IN [✅, ⚠️, ❌]
ASSERT 事件时间线.行数 == 关键流年.count
ASSERT 无绝对断语（不出现"必定""一定""肯定"等词语）
```
# 详见 harness 完整版

### Step 9 Gate
<!-- fix: P1-R4-1 Step 9 Gate Check 与 harness 同步 -->
```
ASSERT 至少1个关键事件有应期推断（应期卡.逐事件应期推断.count >= 1）
ASSERT 每个应期推断有五步流程记录（Step A-E 均有结果标注）
ASSERT 每个应期推断标注了引动方式（T编号 != null）
ASSERT 每个应期推断标注了推理强度（🟢/🟡/🔴）
ASSERT 流月推算方法已标注（五虎遁对照表已引用）
ASSERT 流月推算结果已列出（涉及的关键流年的12月干支）
ASSERT 应期口诀未作为硬规则使用（仅辅助记忆）
```
# 详见 harness 完整版

### Step 10 Gate
<!-- fix: P1-R4-1 Step 10 Gate Check 与 harness 同步 -->
```
ASSERT 日时断语已查询（断语原文 != null OR 标注为"待查"）
ASSERT 六十甲子性质已查表（日柱纳音+象意+喜忌 != null）
ASSERT 纳音大运法已执行（至少6步大运有纳音对比）
ASSERT 十二把金钥匙已查表（至少6步大运有长生状态）
ASSERT 每个交叉结果有标注（[印证/冲突/无关/待查]之一）
ASSERT 交叉验证汇总表已填写
ASSERT 冲突项有详述（冲突数 > 0 时）
```
# 详见 harness 完整版

### Step 11 Gate
<!-- fix: P1-R4-1 Step 11 Gate Check 与 harness 同步 -->
```
ASSERT 大运总卡.大运数 >= 6（每步大运均有评级）
ASSERT 大运总卡.每步字段数 >= 8（不少于8项）
ASSERT 关键事件时间线.count >= 5
ASSERT 关键事件时间线.分散大运数 >= 3
ASSERT 至少1个事件有应期推断（应期窗口 != null）
ASSERT 每个应期推断有引动方式标注（T编号 != null）  # V4b
ASSERT 古籍交叉验证摘要 != null（至少1个验证源有结果）
ASSERT 纳音大运法已执行（至少6步大运有纳音对比）  # V5b
ASSERT 十二把金钥匙已查表（至少6步大运有长生状态）  # V5c
ASSERT 确定性标注.count >= 3（✅ + ⚠️ + ❌ 合计）
ASSERT 校验清单 V1-V8+V4b+V5b+V5c 全部 PASS
ASSERT CA自检 CA1-CA8 全部 PASS
ASSERT 全文无"必定""一定""肯定"（绝对断语检查）
ASSERT 核心结论按确定性降序排列
```
# 详见 harness 完整版

---

## Context Anxiety 防护（与紫微 Phase 5 同规格）

1. **分段执行**：先完成前4步大运（Step 6a），输出中间卡片并自检，再继续后续大运（Step 6b）
2. **密度一致性**：每步大运的分析字段不得少于5个，后面不得比前面粗糙
3. **质量优先于完成度**：宁可只分析6步大运但每步深入，也不要8步但后4步敷衍
4. **关键流年分散性**：5个关键流年应分散在不同大运中
5. **自检信号**：出现"类似前述""不再赘述"等省略语 = 立即停下重新展开

---

## 与现有系统的关系

| 改动 | 文件 | 说明 |
|------|------|------|
| 替代 | `phase7-harness.md` | 新 SOP 替代原 Phase 7 |
| 新增 | `dayun-orchestrator.md` | 本文件 |
| 新增 | `dayun-step0~11-harness.md` | 12 个步骤 harness |
| 新增 | `dayun-reference-tables.md` | 统一查表数据集 |
| 不变 | `phase0-6-harness.md` | 原 Phase 0-6 不变 |
| 不变 | `bazi-evaluator.md` | 评估者不变 |
<!-- fix: P2-R4-2 Phase 8 与 Step 11 报告衔接关系 -->
| 引用 | `phase8-harness.md` 七、大运流年节奏 | Phase 8 报告的"七、大运流年节奏"板块引用 Step 11 输出，此处仅列摘要 |

---

## 调研素材索引

完整规则索引见：`Obsidian/命理/大运流年SOP-规则索引与步骤设计.md`
11 份调研报告见：`Obsidian/命理/调研-*.md`
