# Phase 9: 收敛验证 + Gate Check

> 推理强度：🔴重（交叉验证）
> 输入：Phase 0-8 全部卡片
> 输出：收敛验证报告 + 全流程 Gate Check
> 下一步：最终交付（可选 Phase 10/11）

---

**核心逻辑：** 回顾 Phase 2-8 的所有输出，检查多信号是否收敛。

## 9.1 验证矩阵

对每个被分析的主题/宫位，填写以下矩阵：

```
=== 收敛验证矩阵 ===

主题: [如：事业/10宫]

信号源1 (Model A/B/C): [结论]
信号源2 (D9 校准):     [结论]
信号源3 (Dasha 时间轴): [结论]
信号源4 (Transit):      [结论]
信号源5 (Jaimini):      [结论，如启用]
信号源6 (分盘):         [结论，如使用]

收敛判定:
  ☐ 3+ 信号一致 → ✅ 高置信结论
  ☐ 2 信号一致 → ⚠️ 中置信，标注不确定性
  ☐ 信号矛盾   → ❌ 低置信，列出矛盾点，不下结论
```

**红线规则：** 单一信号来源的结论禁止作为确定性判断输出。必须至少有第二信号佐证。

---

## 9.2 全流程 Gate Check

**目的：** 检查 SOP 每步是否按 harness 规则正确执行。

逐项核对，标记 PASS/FAIL。任何 FAIL 必须回溯修复后才能输出最终报告。

```
=== Gate Check 清单 ===

[Phase 0 数据基础]
☐ Lagna 稳定性测试已执行（±10min）
☐ Ayanamsa 已标注
☐ 边界行星已标注（如有）

[Phase 1 参数完备性]
☐ P1: 7星 + Rahu/Ketu 全部判定身份（共9项）
☐ P1: Sutra 7 (Kendradhipati Dosha) 已执行
☐ P1: Sutra 13 (Rahu/Ketu) 已标注代理身份
☐ P2: 燃烧检查覆盖 5 颗星
☐ P2: 行星战争检查
☐ P2: 逆行标注
☐ P4: SAV 校验和 = 337
☐ P7: 7 星尊贵度全判定
☐ P8: 7 星 Avastha 全计算（含奇偶座正逆序）
☐ P9: 7 星 Shadbala vs 最低阈值逐项对比
☐ P9: Ishta/Kashta 全部提取
☐ P11: Moon Nakshatra 已确认

[Phase 2 Model A]
☐ 9 颗星全部归入 5 种模式之一
☐ 无未归类的星
☐ Rahu/Ketu 走 Sutra 13 特殊路径

[Phase 3 Model B]
☐ 关键星做了完整 5 步检查
☐ Ishta/Kashta 被引用
☐ P9 最低阈值被引用

[Phase 4 Model C]
☐ 每种模式使用了对应公式
☐ 分类变量使用了数值映射表
☐ Yoga 补丁已应用

[Phase 5 D9]
☐ 每颗星执行了身份继承
☐ 内核品质全判定
☐ D9 落宫安全性/毒性检查
☐ Dispositor 状态检查

[Phase 6 宫位诊断]
☐ 管理者 + 租客 + 硬件三层全做
☐ 相位干扰检查
☐ 推荐分盘已标注

[Phase 7 Dasha]
☐ Moon Nakshatra → Dasha 桥梁已引用
☐ 当前 MD/AD 已确认
☐ Dasha 六步法已执行
☐ 格局激活条件已检查
☐ Yogini 交叉验证已执行

[Phase 8 Transit]
☐ 过境从 Moon sign 算起
☐ Vedha 遮蔽检查已执行
☐ Double Transit 交集已计算
☐ Sade Sati 状态已确认
☐ Dasha-Transit 集成已执行

[Phase 9 收敛]
☐ 每个主题至少 2 个独立信号源
☐ 三级置信判定已标注
☐ 矛盾信号已标注且未下确定性结论

=== Gate Check 结果 ===
PASS: [X] / FAIL: [Y]
若 FAIL > 0 → 列出失败项 → 回溯修复 → 重新 Gate Check
若 FAIL = 0 → ✅ SOP 执行质量合格，最终报告可输出
```

---

## OUTPUT: 收敛验证报告

```
=== 最终综合报告 ===
【盘面底色】: [一句话概括此人的命盘核心特征]
【最强资产】: [哪个领域/宫位最突出？多信号支撑]
【最大风险】: [哪个领域/宫位最脆弱？多信号支撑]
【当前窗口】: [当前 Dasha + Transit 的综合研判]
【关键预测】: [只列出高置信结论，低置信的用 ⚠️ 标注]

=== Gate Check 结果 ===
PASS: [X] / FAIL: [Y]
状态: [✅ 合格 / ❌ 需回溯修复]
```

---

## Gate Check

```
ASSERT 每个分析主题至少有 2 个独立信号源
ASSERT 三级置信判定已标注（高/中/低）
ASSERT 矛盾信号已标注且未下确定性结论
ASSERT 最终报告包含：盘面底色 / 最强资产 / 最大风险 / 当前窗口 / 关键预测
ASSERT 单一信号来源的结论未作为确定性判断输出
ASSERT 全流程 Gate Check FAIL = 0
```
