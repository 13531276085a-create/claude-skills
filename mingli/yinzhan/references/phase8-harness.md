# Phase 8: Transit + Vedha 过境叠加

> 推理强度：🟡中（叠加计算）
> 输入：Phase 7 Dasha 时间轴卡
> 输出：Transit 叠加卡
> 下一步：Phase 9（连续执行）

---

**原则：** Transit = 催化剂，不是决定因素。Dasha 创造事件条件，Transit 触发具体时机。

## 8.1 过境参考点

**从 Moon sign（Janma Rashi）算起**，不从 Lagna 算。这是 Jyotish 与西方占星的根本区别。

## 8.2 吉凶过境位 + Vedha 遮蔽表

| 行星 | 吉位（从 Moon） | Vedha 遮蔽位 |
|------|----------------|-------------|
| Sun | 3, 6, 10, 11 | 9, 12, 4, 5 |
| Moon | 1, 3, 6, 7, 10, 11 | 5, 9, 12, 2, 4, 8 |
| Mars | 3, 6, 11 | 12, 9, 5 |
| Mercury | 2, 4, 6, 8, 10, 11 | 5, 3, 9, 1, 8, 12 |
| Jupiter | 2, 5, 7, 9, 11 | 12, 4, 3, 10, 8 |
| Venus | 1, 2, 3, 4, 5, 8, 9, 11, 12 | 8, 7, 1, 10, 9, 5, 11, 6, 3 |
| Saturn | 3, 6, 11 | 12, 9, 5 |

**Vedha 规则：** 即使行星过境吉位，若另一星同时过境对应的 Vedha 位 → 吉果被遮蔽。
**例外：** Sun 和 Saturn 互不遮蔽。

## 8.3 Double Transit Theory（双重过境）

**当 Jupiter 和 Saturn 同时 aspect 某宫位时，该宫位事件大概率触发。**

检查方法：
1. Jupiter 当前位置 → aspect 哪些宫（自身 + 5th + 7th + 9th）
2. Saturn 当前位置 → aspect 哪些宫（自身 + 3rd + 7th + 10th）
3. 交集 = 双重过境激活的宫位

## 8.4 Ashtakavarga 过境过滤器

过境行星经过某星座时，查该星在该座的 BAV 分值：
- BAV ≥ 5: 过境效果放大（吉/凶均放大）
- BAV = 4: 中性
- BAV ≤ 3: 过境效果减弱

## 8.5 关键过境追踪

| 过境 | 周期 | 意义 |
|------|------|------|
| **Sade Sati** | ~7.5 年 | Saturn 过 Moon 前后各一座。Phase 1(12th)=压力起; Phase 2(1st)=最高压; Phase 3(2nd)=家庭/财务 |
| **Jupiter Transit** | ~13 个月/座 | 扩张、机遇 |
| **Saturn Transit** | ~2.5 年/座 | 纪律、业力考验 |
| **Rahu-Ketu Transit** | ~18 个月/轴 | 业力激活、突变 |

## 8.6 Dasha-Transit 集成公式

```
Dasha lord 过境状态:
  - 过境自旺/入庙/友宫 = Dasha 正面效果放大
  - 过境落陷/敌宫/燃烧 = Dasha 负面效果放大

Moon 过境 Dasha lord 的旺位 或 从 Dasha lord 算起的 3/5/6/7/9/10/11 宫
  = 触发该 Dasha 的具体正面事件

结论: "Dasha 说会发生什么; Transit 说发生的时候你感觉如何"
```

---

## OUTPUT: Transit 叠加卡

```
=== Transit 过境分析 ===
当前重大过境: [列出 Jupiter/Saturn/Rahu-Ketu 当前位置及影响]
Sade Sati 状态: [是否在 Sade Sati 中？Phase ?]
Double Transit 激活宫位: [列出]
Vedha 遮蔽: [列出被遮蔽的吉位]

=== Dasha × Transit 叠加 ===
当前 Dasha + 当前 Transit = [综合判断]
近期关键触发窗口: [具体日期/月份]
```

---

## Gate Check

```
ASSERT 过境从 Moon sign 算起（非 Lagna）
ASSERT Vedha 遮蔽检查已执行
ASSERT Double Transit 交集已计算
ASSERT Sade Sati 状态已确认
ASSERT Dasha-Transit 集成已执行
```
