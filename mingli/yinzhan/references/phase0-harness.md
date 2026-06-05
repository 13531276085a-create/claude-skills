# Phase 0: Lagna 稳定性验证

> 推理强度：🟢轻（校验）
> 输入：用户提供的印占 PDF
> 输出：基础验证卡
> 下一步：Phase 1（等用户确认后）

---

## 0.1 Lagna 稳定性测试

**强制检查：** 出生时间 ±10 分钟是否导致 Lagna（上升星座）换座。

| 场景 | 处理 |
|------|------|
| ±10 分钟 Lagna 不变 | 安全，继续 |
| ±10 分钟 Lagna 换座 | **边界盘**，必须标注。提供两版 Lagna 的对比分析 |
| 出生时间不确定（>30 分钟误差） | 标记为**不可靠盘**，仅做定性分析，不做精确预测 |

## 0.2 Ayanamsa 确认

| Ayanamsa | 适用场景 |
|----------|---------|
| **Lahiri**（默认） | 印度官方标准，大多数情况 |
| KP Ayanamsa | 使用 KP 系统时 |
| Raman | B.V. Raman 体系 |

**规则：** 不同 Ayanamsa 可能导致行星换座。报告中必须注明使用的 Ayanamsa。若边界行星在不同 Ayanamsa 下换座，提供两版对比。

## 0.3 宫位制确认

- 默认：**整宫制 (Whole Sign Houses)** = Jyotisha 标准
- Lagna 所在星座 = 完整1宫，下一星座 = 2宫，依此类推
- 每宫 = 完整30度
- **不使用** Placidus / Koch 等西方不等宫制（KP 可选模块除外）

---

## OUTPUT: 基础验证卡

```
=== 基础验证卡 ===
Lagna: [星座] [度数]
Lagna 稳定性: [安全 / 边界盘(±Xmin换座) / 不可靠盘]
Ayanamsa: [Lahiri / KP / Raman]
宫位制: 整宫制
边界行星: [列出在不同 Ayanamsa 下可能换座的星，如无则"无"]
```

**输出后等待用户确认基础数据可靠性，方可进入 Phase 1。**

---

## Gate Check

```
ASSERT Lagna 稳定性测试已执行（±10min）
ASSERT Ayanamsa 已标注
ASSERT 宫位制已确认
ASSERT 边界盘/不可靠盘已标注（如有）
```
