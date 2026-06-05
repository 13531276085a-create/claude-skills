# Phase 5: D9 校准 + Jaimini 交叉验证

> 推理强度：🔴重（多层审计）
> 输入：Phase 1 参数卡 + Phase 2-4 Model A/B/C 审计卡
> 输出：D9 结算卡
> 下一步：Phase 6（等用户选宫位）

---

## STEP 5.0: 身份继承 (Identity Inheritance)

**核心指令:** 继承 D1 的 P1 身份偏置，执行"品质核验"与"最终结算"。禁止在该模块预测事件，仅针对 D1 承诺的"质量"与"代价"进行结构化评估。

- **强制偏置:** 该行星必须携带 D1 的 P1 身份（忠诚/交易/掠夺）。
- **逻辑转换:**
  - [D1 掠夺者] + [D9 强] = 破坏力/收割力增强
  - [D1 忠诚者] + [D9 弱] = 保护力失效

## STEP 5.1: 资产合规性审计 (Integrity Audit)

**内核品质 (Sign Quality):**

| D9 星座状态 | 等级 | 兑现率 |
|-------------|------|--------|
| Vargottama (同宫) | 钻石 | 结构极稳，0损耗兑现 |
| 入旺/本宫 | 金/银 | 100% 兑现，能量正向增益 |
| 友/中/敌宫 | 铜/铁/铅 | 50%-80% 兑现，存在平庸化风险 |
| 落陷 (Debilitated) | 废铁 | 彻底违约，成果腐烂或转化为负债 |

**安全性/毒性检查 (House Security):**

| D9 落宫 | 判定 | 说明 |
|---------|------|------|
| 1/2/4/5/7/9/10/11 | 合规资产 | 存入金库，收益可自主支配 |
| 3/6 | 争议资产 | 需通过竞争或高强度劳动变现 |
| 8 | 有毒-毁灭 | 极度严重（系统崩溃/反噬） |
| 12 | 有毒-耗散 | 严重（得而复失/白忙一场） |

*补丁：除非触发 Pushkara (滋养点)，否则 8/12 宫直接判定为"因得招祸"或"得而复失"。*

**严重程度排序:** D9落8宫 > D9落12宫 > D9星座落陷 > D9落6宫

## STEP 5.2: 环境兼容性分析 (Environment Check)

- **D9 房东状态:** 该行星落宫的 Dispositor 在 D9 的强度。若房东落陷 = "金库被盗/支票无法兑现"。
- **D9 Lagna 适配:** 该星在 D9 上升下的功能吉凶。若为 D9 功能凶星 = "外部成功的内部代价"。

## STEP 5.3: 最终结算报告 (Final Settlement)

```
【能量位移】: 从 D1 [宫位/战场] → D9 [宫位/归宿]
【身份偏置】: 继承自 D1 的 [P1属性] 在 D9 被 [放大/削弱/扭曲]
【真伪鉴定】: [真金/白银/青铜/废铁]（基于 D9 星座）
【合规判定】: [安全/风险/有毒]（基于 D9 落宫及房东状态）
【最终结算单】: 总结该资产是"增值的原始股"、"高利的印钞机"还是"带毒的诱饵"

【终极结论】
实战成败判定: [成功/平庸/失败]
代价/副作用: 明确指出由于 Identity_Bias 带来的系统误差
架构师建议: [如：主动变现、隔离资产、或接受磨损]
```

---

## STEP 5.5: [可选] Jaimini 交叉验证

**触发条件：** 用户要求多学派验证，或 Phase 2-5 中出现矛盾信号需要第二意见。

**⚠️ 关键警告：** Parashari 和 Jaimini 有本质差异（相位规则、Karaka 类型、Dasha 类型均不同），不可混用。此步骤是独立的第二视角，不是 Parashari 分析的补丁。

### Chara Karakas 计算（按经度排序）

| Karaka | 确定方法 | 代表 |
|--------|---------|------|
| **Atma Karaka (AK)** | 经度最高的行星 | 灵魂/自我/此生核心课题 |
| **Amatya Karaka (AmK)** | 经度第二 | 事业/财富/世俗成就 |
| **Bhratri Karaka (BK)** | 经度第三 | 兄弟姐妹 |
| **Matri Karaka (MK)** | 经度第四 | 母亲 |
| **Putra Karaka (PK)** | 经度第五 | 子女 |
| **Jnathi Karaka (GK)** | 经度第六 | 敌人/疾病 |
| **Dara Karaka (DK)** | 经度最低 | 配偶 |

### Karakamsha 分析

AK 在 D9 (Navamsha) 的位置 = **Karakamsha Lagna**，映射回本命盘，分析灵魂层面的人生方向。

### Jaimini Rashi Aspects（星座相位）

- **Cardinal 座 (Aries/Cancer/Libra/Capricorn)** 看所有 Fixed 座（除相邻的那个）
- **Fixed 座 (Taurus/Leo/Scorpio/Aquarius)** 看所有 Cardinal 座（除前一个）
- **Dual 座 (Gemini/Virgo/Sagittarius/Pisces)** 看所有其他 Dual 座

**⚠️ 这是 Cardinal/Fixed/Dual 分类，不是阳性/阴性分类，两者不同。**

### OUTPUT（如启用 Jaimini）

```
=== Jaimini 交叉验证 ===
AK=[行星] (灵魂课题: [描述])
AmK=[行星] (事业载体: [描述])
DK=[行星] (配偶特质: [描述])
Karakamsha=[星座/宫位] → 灵魂方向: [描述]

与 Parashari 结论对比:
- 一致点: [列出]
- 矛盾点: [列出] → 标注需进一步验证
```

---

## Gate Check

```
ASSERT 每颗星都执行了身份继承（D1 P1 → D9）
ASSERT 内核品质（Vargottama/旺/庙/友/中/敌/陷）全判定
ASSERT D9 落宫安全性/毒性检查（8/12宫标记有毒）
ASSERT Dispositor 状态检查
IF Jaimini 启用 THEN Chara Karakas 已计算 + Karakamsha 已分析
```
