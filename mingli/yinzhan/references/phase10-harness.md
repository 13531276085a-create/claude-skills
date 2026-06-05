# Phase 10: [可选] KP 精确定时模块

> 推理强度：🟡中（独立视角）
> 输入：Phase 1 参数卡
> 输出：KP 定时卡
> 触发条件：用户需要精确到月级的事件定时（如："什么时候结婚？"）

---

**⚠️ KP 使用 Placidus 宫位制（不等宫），与主流程的整宫制不同。此模块是独立视角。**

## KP Sub-Lord 核心逻辑

每个 Nakshatra (13°20') 被进一步分为 9 个不等的 Sub，按 Vimshottari 比例分配：

**分析层级：**
1. **Sign Lord（星座主）** = 事件的来源/环境
2. **Star Lord（星宿主）** = 事件的性质/结果类型
3. **Sub Lord（子分主）** = 事件是否真的发生（决定性因素）

## KP Significator 四级优先级

| 级别 | 来源 | 力量 |
|------|------|------|
| A（最强） | 宫内行星的 Nakshatra 上有其他星 | 最强 significator |
| B | 宫内行星本身 | 强 |
| C | 宫主星的 Nakshatra 上有其他星 | 中 |
| D（最弱） | 宫主星本身 | 弱（仅当 ABC 无对应时启用） |

## KP 四步预测法

1. 确定相关宫位的宫头 (cusp)
2. 找到该 cusp 的 Star Lord
3. 找到 Star Lord 范围内的 Sub Lord
4. Sub Lord 的 significator houses 决定事件吉凶

## CSL 事件承诺检查（KP 最独特的机制）

**先判断"能不能发生"，再判断"什么时候"。**

1. 找到目标宫位的 Cuspal Sub Lord (CSL)
2. 确定 CSL 的 significator houses（用四级优先级方法）
3. 若 CSL signify 有利宫位组 → 事件被承诺 ✅
4. 若 CSL signify 否定宫位组 → 事件被拒绝 ❌（无论 Dasha 多好）

## 主要事件的宫位组合速查

| 事件 | 有利宫位 | 否定宫位（12th-house 否定规则）|
|------|---------|------|
| **结婚** | 2, 7, 11 | 1, 6, 10 |
| **恋爱结婚** | 5, 7, 11 | 4, 6, 10 |
| **事业/工作** | 2, 6, 10, 11 | 1, 5, 8, 12 |
| **升职** | 2, 6, 10, 11 | 5, 8, 12 |
| **出国** | 3, 9, 12 | — |
| **子女** | 2, 5, 11 | 1, 4, 10 |
| **买房** | 4, 11 | 3, 10 |
| **财富** | 2, 6, 11 | 1, 5, 12 |
| **离婚** | 1, 6, 10 (+ 8, 12) | — |

## Ruling Planets（当下活跃行星）

咨询时刻的五颗活跃行星（当下时间锚点）：
1. Lagna Star Lord（最强）
2. Moon Star Lord
3. Lagna Sign Lord
4. Moon Sign Lord
5. Day Lord（最弱）

**验证规则：** 若 natal chart 的 significators 出现在 Ruling Planets 中 → 事件"已成熟"，近期触发。不出现 → 时机未到。

## RP 定时精度

| 时间范围 | 用什么行星过境 |
|---------|-------------|
| 具体哪天 | Lagna 过境 sensitive star-sub |
| 30 天内 | Moon 过境 sensitive star-sub |
| 1 年内 | Sun 过境 sensitive zones |
| 1-5 年 | Jupiter 过境 sensitive zones |

---

## OUTPUT: KP 定时卡

```
=== KP 精确定时 ===
目标问题: [用户的具体问题]
相关宫位: [KP 分析的 cusp]

CSL 承诺检查:
  Cusp Sub Lord: [行星]
  Significators: [宫位列表]
  有利组匹配: [✅ 承诺 / ❌ 拒绝]

Significator 层级:
  A级: [行星列表]
  B级: [行星列表]
  C级: [行星列表]

事件定时:
  Dasha 窗口: [Vimshottari 指向的时段]
  RP 验证: [当前 Ruling Planets 是否匹配？]
  精确触发: [Moon/Sun 过境 sensitive 点的日期]

判定: [事件是否会发生？何时？置信度]
```

---

## Gate Check

```
ASSERT CSL 承诺检查已执行
ASSERT Significator 四级优先级已按规则计算
ASSERT Ruling Planets 已列出
IF 事件被承诺 THEN 定时精度已给出
IF 事件被拒绝 THEN 已明确告知用户
```
