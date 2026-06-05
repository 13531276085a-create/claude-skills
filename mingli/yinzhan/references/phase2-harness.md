# Phase 2: Model A - D1 模式判定

> 推理强度：🟡中（分类决策）
> 输入：Phase 1 P1-P13 参数卡
> 输出：Model A 审计卡
> 下一步：Phase 3（连续执行）

---

## 模式分类

根据 P1-P13 参数，对每颗关键行星判定其运行模式。

基于 P1(身份) + P8(司机状态) 组合判定：

| 模式 | P1 身份 | P8 司机 | 隐喻 |
|------|--------|--------|------|
| **创始人 (Founder)** | 吉 | 青/少 | 自己人+主动驾驶 = 核心创造者 |
| **吉祥物 (Mascot)** | 吉 | 老/婴/死 | 自己人但被动 = 名义持有者 |
| **雇佣兵 (Mercenary)** | 凶 | Yuva/Kumara | 外人但能打 = 高效但有代价 |
| **职业经理人 (Agent)** | 中 | 任意 | 中间人 = 平台决定上限 |
| **飘萍 (Drifter)** | 凶 | Baala/Vriddha/Mrita | 外人+被动 = 纯看命 |

**P8 简化说明：** Model A 将 P8 五阶段（Baala/Kumara/Yuva/Vriddha/Mrita）压缩为二分法——主动（Yuva+Kumara）vs 被动（Baala+Vriddha+Mrita）。细粒度差异在 Model B 代价计算中体现。

**Rahu/Ketu 特殊路径：** 不走常规 P1 判定。按 Sutra 13 规则，取所在宫主 + 合相星的身份作为 Rahu/Ketu 的代理身份。

---

## OUTPUT: Model A 审计卡

```
=== Model A 审计结果 ===
[行星名]: [模式] | P1=[身份] | P8=[司机] | P7=[车型] | 落宫=[X宫]
...（逐颗行星列出，含 Rahu/Ketu，共9项）
```

---

## Gate Check

```
ASSERT 9 颗星（含 Rahu/Ketu）全部归入 5 种模式之一
ASSERT 无未归类的星
ASSERT Rahu/Ketu 走 Sutra 13 特殊路径
ASSERT OUTPUT BLOCK A 完整输出
```
