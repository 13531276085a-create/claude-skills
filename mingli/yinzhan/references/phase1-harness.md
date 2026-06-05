# Phase 1: 盘面解析与参数确认（P1-P13）

> 推理强度：🟢轻（查表填空）
> 输入：Phase 0 基础验证卡 + PDF 盘面数据
> 输出：P1-P13 参数卡
> 下一步：Phase 2（等用户确认后）

---

读取 PDF 后，按以下参数框架 (P1-P13) 解析每颗行星：

## THE PROTOCOL: 命理物流工程模型 (The Logistics Model)

### P1. 身份/立场 (Identity) - 行星**掌管**宫位（Lordship，非落入位置）

**⚠️ P1 判据 = 行星掌管（own）哪些宫位。P5 判据 = 行星落入（placed in）哪个宫位。两者不同，勿混淆。**

- **定义:** 三角宫 (1/5/9) 宫主是忠诚者 (吉)。其他按掌管宫位分类。
- 判断逻辑：
  - **Loyalist（忠诚者）**: 掌管 1/5/9 宫的星（Trikona lords）
  - **Trader（交易者）**: 掌管 2/4/7/10 宫的星（Kendra lords + 2nd）
  - **Hostile（掠夺者）**: 掌管 3/6/8/11/12 宫的星（Dusthana + Trishadaya）
  - 双宫主 → 以 Trikona 身份优先（如 Aries Lagna 的 Mars = 1L+8L → Loyalist）
- **偏置信号:** 掠夺者是一个带偏置 (Bias) 的信号。力量越强 = 信号越强 = 成功度越高，但系统误差（代价/副作用）也越明显。

**Laghu Parashari 硬规则（必须执行）：**

| 规则编号 | 内容 | 隐喻 |
|---------|------|------|
| Sutra 7 | **Kendradhipati Dosha**: 自然吉星（Jupiter/Venus/Mercury/Moon）掌管 Kendra (1/4/7/10) → 失去吉性，变中性偏凶。自然凶星掌管 Kendra → 失去凶性，变中性偏吉 | 好人当官被腐蚀，坏人当官反而守规矩 |
| Sutra 13 | **Rahu/Ketu 规则**: Rahu/Ketu 给出它们所在宫位的宫主星 + 合相星的结果 | 变色龙——穿谁的衣服就演谁 |
| Sutra 20 | **Yoga Karaka**: 单星同时掌管 Kendra + Trikona → 超级忠诚者 | 身兼两职的核心高管 |

---

### P2. 行星健康度 (System Health)

- **燃烧 (Combustion):** 资源虽然存在，但管理权限被太阳（皇权/意志）强行收缴。
  - 燃烧距离阈值：Mars<17° / Mercury<14°(顺)/12°(逆) / Venus<10° / Jupiter<11° / Saturn<15°
  - Moon 与 Sun 接近为 Amavasya（新月），由 Paksha Bala 处理，不按燃烧判定
  - Rahu/Ketu 为 Chaya Graha（影子星体），不适用燃烧规则
- **行星战争 (Planetary War):** 系统死锁。两颗行星在1°内，能量无法对外输出。
  - **胜负判定：** 经度更高者（在星座中度数更大者）为胜方。战败方减力严重（约减 50%+）。
  - Sun 不参与行星战争（Sun 的规则是燃烧，不是战争）。
- **P2.2 逆行**——【高压变频/重复做功】
  - 吉身份逆行：动力反复输出，虽然慢，但单点压强极高，适合深度研发（Debug）。
  - 凶身份逆行：破坏力加倍且带有"回马枪"属性。

---

### P3. 仓库 (Warehouse) - 行星掌管宫位与合相

- P3.1 基础货物: 掌管宫位的原始性质（如 6宫=债务/同时掌管两个宫位则货物捆绑）。
- P3.2 结构耦合 (合相):
  - **合相定义：** 同一星座内即算合相。距离越近效果越强：<5° = 紧密合相（强耦合）; 5-15° = 松散合相; >15° 同座 = 微弱合相。
  - **双吉合相:** 1+1 > 2 (资源共享/仓库合并)。
  - **吉凶混杂:** 资源污染。你的"占有权"被稀释（想调动福报，必须同时触发灾难）。

---

### P4. 库存量 SAV (Inventory Bandwidth) - 掌管宫位SAV

逻辑: 后台仓库有货吗？

| SAV 范围 | 评级 | 含义 |
|----------|------|------|
| < 20 | 断供区/空心化 | "有名无实"。有头衔没实权，项目无法落地 |
| 20-25 | 高阻区/低效 | "高维护成本"。必须通过超负荷的个人努力才能维持 |
| 26-32 | 平稳区 | "正常供货"。供需平衡，符合世俗平均水平 |
| > 32 | 溢出区 | "自动驾驶/超导"。后台资源溢出，推着你往前走 |

*特殊规则:* 8宫(灾难) < 20 是**大吉**(安全/绝缘)。11宫(收益) < 20 是**赤贫**。

**Shodhana 精修（可选深度路径）：**
若需更精确评估，可对 Ashtakavarga 执行两步净化：
1. **Trikona Shodhana（三角减值）**: 将 12 宫分成 4 组三角宫（火/土/风/水），每组中最小值从三宫中减去
2. **Ekadhipatya Shodhana（一主减值）**: 对双宫主星（Mars/Venus/Mercury/Jupiter/Saturn），比较两宫减后值，小值从大值中减去
3. 净化后的 SAV 更接近"净利润"而非"毛收入"

**校验和：** 7 颗星的原始 SAV 总和恒等于 **337**（数学常数）。若不等 = 数据错误。

---

### P5. 路段类型 (Road Type) - 落宫性质

| 路段类型 | 宫位 | 性质 | 损耗率 |
|---------|------|------|--------|
| **Kendra（支柱）** | 1/4/7/10 | 四大支柱，显性力量 | ≈ 0% |
| **Trikona（福报）** | 5/9 | Lakshmi 之所，最吉 | ≈ 0% |
| **中性-2宫** | 2 | 家庭/财富/言语，中性偏吉 | ≈ 5-10% |
| **Upachaya（成长）** | 3/6/10/11 | **凶星在此反而好**（随时间改善） | 10-30% |
| **凶路-6宫** | 6 | 摩擦力、重复劳动、调试 | ≈ 30% |
| **凶路-8宫** | 8 | 系统风险、黑箱操作 | ≈ 40% |
| **凶路-12宫** | 12 | 能量耗散、隐性维护费 | ≈ 50% |

**Upachaya 关键规则（BPHS 确认，4+ 源一致）：** 自然凶星（Mars/Saturn/Sun/Rahu）落入 3/6/10/11 宫 = 吉。这些宫位的特点是"随时间改善"，凶星的压力反而转化为竞争力。吉星在 Upachaya 反而平庸。

**双重归属优先级规则：** 10 宫同属 Kendra + Upachaya，取 Kendra 损耗（0%）。6 宫同属 Upachaya + Dusthana，损耗按 Dusthana 优先（30%），但凶星在此按 Upachaya 规则获益。

- *注：在"隔离环境"（科研/海外/灵修）下，12宫折损率可反转为"增益率"。*

---

### P6. 路况 SAV (Road Condition) - 落入宫位SAV

| SAV 范围 | 评级 | 损耗率 |
|----------|------|--------|
| > 32 | 超导路段 | 0% 损耗，加速度 > 1g |
| 26-32 | 顺风路段 | 10-20% 损耗 |
| 20-25 | 逆风路段 | 40-60% 损耗 |
| < 20 | 崩塌路段 | > 80% 损耗，车毁人亡风险 |

- *凶星悖论:* 8宫/危机：高 SAV = "瞬间毁灭/爆雷"；低 SAV (<20) = "僵局/安全/慢性隐患"。

---

### P7. 车的档次 (Car Grade) - 落入星座（尊贵度）

| 尊贵度 | 隐喻 | 说明 |
|--------|------|------|
| 入旺 (Exalted) | F1 赛车 | 性能拉满，但难驾驭，通用性差 |
| MT (Moolatrikona) | 高性能特种车 | 执行公务的最佳状态（优于入庙） |
| 入庙 (Own Sign) | 私家豪车 | 舒适，稳定，资源自主 |
| 友宫 (Friendly) | 朋友的车 | 基本够用 |
| 中性 (Neutral) | 租车 | 不好不坏 |
| 敌宫 (Enemy) | 陌生人的车 | 不顺手 |
| 落陷 (Debilitated) | 错配车/故障车 | 坦克上高速，跑车下泥地 |

**旺度/陷度精确度数表（BPHS）：**

| 行星 | 入旺星座 | 旺度 (Deep Exalt.) | 落陷星座 | 陷度 |
|------|---------|-------------------|---------|------|
| Sun | Aries | 10° | Libra | 10° |
| Moon | Taurus | 3° | Scorpio | 3° |
| Mars | Capricorn | 28° | Cancer | 28° |
| Mercury | Virgo | 15° | Pisces | 15° |
| Jupiter | Cancer | 5° | Capricorn | 5° |
| Venus | Pisces | 27° | Virgo | 27° |
| Saturn | Libra | 20° | Aries | 20° |

- **NBRY 补丁 (逆袭):** 若定位星强力或在四正宫 = "废土改装战车"。起步极低，上限极高。

---

### P8. 司机状态 (Driver Status) - 行星年龄状态

| 状态 | 驾驶模式 | 说明 |
|------|----------|------|
| 青/少 (Yuva/Adult) | 主动驾驶 | 你是主宰，成败算你的 |
| 婴 (Baala/Infant) | 辅助驾驶-需喂养 | 依赖资源输入 |
| 老 (Vriddha/Old) | 辅助驾驶-靠经验 | 依赖过去积累 |
| 死 (Mrita/Dead) | 无人驾驶/宿命点 | 脚本自动执行，你只是乘客 |

**行星年龄计算（Avastha，基于 BPHS）：**
将行星在星座内的度数（0-30°）映射到年龄阶段。规则取决于星座奇偶性：
- **奇数座**（Aries/Gemini/Leo/Libra/Sag/Aqua）: 0-6°=Baala → 6-12°=Kumara → 12-18°=Yuva → 18-24°=Vriddha → 24-30°=Mrita
- **偶数座**（Taurus/Cancer/Virgo/Scorpio/Cap/Pisces）: **反序** 0-6°=Mrita → 6-12°=Vriddha → 12-18°=Yuva → 18-24°=Kumara → 24-30°=Baala

---

### P9. 基础功率 (Shadbala) - 行星力量分

**总力评估：**
- **> 1.0 (100%):** 健康。点火就着，爬坡有力。
- **0.8-1.0:** 亚健康。偶尔掉链子。
- **< 0.8 (Fail):** 积碳/亏电。关键时刻掉链子/熄火。

**六力组成：**

| 力 | 梵文 | 含义 | 关键规则 |
|----|------|------|---------|
| 位置力 | Sthana Bala | 旺/庙/友/敌 | 入旺最高，落陷最低 |
| 方向力 | Dig Bala | 方位适配 | Jupiter+Mercury 强在东(1宫); Sun+Mars 强在北(10宫); Saturn 强在西(7宫); Venus+Moon 强在南(4宫) |
| 时间力 | Kala Bala | 昼夜/季节 | Moon+Mars+Saturn 夜间强; Sun+Jupiter+Venus 白天强; Mercury 恒强 |
| 运动力 | Cheshta Bala | 速度/逆行 | 慢速/逆行 = 高 Cheshta（聚焦能量）|
| 天然力 | Naisargika Bala | 固有等级 | Sun > Moon > Venus > Jupiter > Mercury > Mars > Saturn |
| 相位力 | Drik Bala | 被谁看 | 被吉星看 = 加分，被凶星看 = 减分 |

**Ishta-Kashta 二分法：**
Shadbala 内含两个子指标，必须同时检查：
- **Ishta Phala（吉分）**: 这颗星能给你多少好处（建设性输出上限）
- **Kashta Phala（凶分）**: 这颗星能造多少麻烦（破坏性输出上限）
- 高 Ishta + 低 Kashta = 纯吉；高 Kashta + 低 Ishta = 纯凶；双高 = 大起大落

**最低 Shadbala 阈值（Rupas）：**
Sun ≥ 5.0 | Moon ≥ 6.0 | Mars ≥ 5.0 | Mercury ≥ 7.0 | Jupiter ≥ 6.5 | Venus ≥ 5.5 | Saturn ≥ 5.0

---

### P10. 交通信号 (Aspects) - Graha Drishti (行星相位)

- **吉星相位:** 空中加油 / 救援队。
- **凶星相位:**
  - 火星: 撞击 / 剐蹭事故 (Collision)。
  - 土星: 红灯 / 严重拥堵 (Delay)。

**相位强度表（BPHS）：**

| 行星 | 7th 相位 | 特殊相位 1 | 特殊相位 2 |
|------|---------|-----------|-----------|
| 所有行星 | 100% (Full) | — | — |
| Mars | 100% | 4th = 75% | 8th = 100% |
| Jupiter | 100% | 5th = 50% | 9th = 100% |
| Saturn | 100% | 3rd = 75% | 10th = 100% |

- Rahu/Ketu：Parashari 传统不赋予特殊相位（争议项，标注即可）
- 百分比 = 该相位影响力相对于满相位的比例

---

### P11. 星宿驱动 (Nakshatra Layer) - 核心动力特征（扩展版）

**P11.1 星宿主身份：** 若星宿主在 D1 为吉身份，赋予该行星 [软着陆] 属性。若为凶身份，底层驱动有毒。

**P11.2 星宿本质特征：** 如 Krittika (切割/尖锐), Rohini (滋养/生长), Ashlesha (纠缠/操控)。

**P11.3 Pada 定位：**
每个 Nakshatra 分为 4 个 Pada（各 3°20'），每个 Pada 对应一个 Navamsha 星座。
- Pada 1 = Dharma（目标导向）
- Pada 2 = Artha（资源导向）
- Pada 3 = Kama（欲望导向）
- Pada 4 = Moksha（超脱导向）

Pada 是 D1→D9 的精确桥梁。27 宿 × 4 Pada = 108 Navamsha。

**P11.4 属性速查：**
每颗行星所在 Nakshatra 需记录：

| 属性 | 含义 | 用途 |
|------|------|------|
| **Gana（气质）** | Deva(天)/Manushya(人)/Rakshasa(魔) | 性格底色、婚配 |
| **Guna（质性）** | Sattva(纯)/Rajas(动)/Tamas(惰) | 行为驱动力 |
| **Animal（动物象征）** | 如 Ashwini=马, Bharani=象 | 本能模式 |
| **Deity（主神）** | 守护能量来源 | 灵性层面 |

**P11.5 Vimshottari 起点：** Moon 所在 Nakshatra 决定了整个 Dasha 序列的起点。这是 P11 最关键的功能输出——它连接了静态盘面（P1-P10）和时间轴（Phase 7）。

**27 宿详细属性参考：** 查阅 Obsidian 知识库 `[[印占]]` 中的 Nakshatra 章节，或使用 Jagannatha Hora 软件的 Nakshatra 面板获取精确属性。

---

### P12. 格局算法 (Yogas Audit) - 系统集成电路

**S 级格局：**
- Dharma-Karma Yoga (9-10 联动): 系统级溢价，大幅对冲 P1 的负偏置。
- Pancha Mahapurusha Yoga: Mars/Mercury/Jupiter/Venus/Saturn 在自旺/入庙且在 Kendra。

**A 级格局：**
- Raja Yoga (Kendra 主 + Trikona 主联动，形成方式：合相/互相位/换座 Parivartana)
- Dhana Yoga (2/5/9/11 宫主联动)
- Viparita Raja Yoga (Dusthana 主在另一 Dusthana = 逆境翻盘)

**B 级格局：**
- Gaja Kesari Yoga (Jupiter 在 Moon 的 Kendra)
- Amala Yoga (吉星在10宫)
- Budhaditya Yoga (Sun + Mercury 合相)

**格局失效条件：** 参与星被燃烧/行星战争/落陷无救 → 格局减效或失效。

**格局激活条件（关键）：** Yoga 只在参与星的 Dasha 期间激活。未到 Dasha = 潜伏资产。

**⚠️ Karaka Bhava Nasha 警告：**
当自然 Karaka 落入自己的 Karaka 宫位时（如 Jupiter=5宫自然 Karaka 落入5宫），可能反伤该宫事项。

**经典依据：** Bhavartha Ratnakara Ch.2 Sl.9 — "very little of their indications"（减弱而非毁灭）。BPHS 中无明确原文。

**KBN 生效条件（全部满足才激活）：**
- 该 Karaka 同时被凶星相位/合相
- 该 Karaka 落陷/敌宫/力弱
- 对应分盘（如 D7 for 子女）中也确认弱化

**KBN 取消条件（任一即取消）：**
- 入旺 (Exalted) 或入庙 (Own Sign) → 完全取消
- 友宫 + 吉星相位 → 大幅减轻
- Moon 入4宫 → 公认例外（母爱深厚而非伤母）
- Saturn 入8宫 → BV Raman 专门标注例外（不减寿）
- Jupiter 入2宫 → BV Raman 标注例外（不损财）

**⚠️ Jupiter-5th 争议：** 统计数据（1571 盘样本）显示 Jupiter 入5宫者大家庭比例反而高 13%。Saptarishi Nadi 明确记载 Jupiter 入5有利子女。此对最不可靠。

**底线：** 条件性标记，非确定性规则。最可靠场景 = 凶星(Mars/Saturn) + 弱化状态 + 无吉星支援

**Karaka-宫位对应表：**

| Karaka | 宫位 | 场景 |
|--------|------|------|
| Sun | 1宫 | 自我过度 → 健康/个性问题 |
| Jupiter | 2宫 | 财富教育过度保护 → 反伤 |
| Mars | 3宫 | 勇气过度 → 冲突 |
| Moon | 4宫 | 情感依赖 → 安全感缺失 |
| Jupiter | 5宫 | 智慧/子女 → 过度干预 |
| Mars/Saturn | 6宫 | 敌人/疾病 |
| Venus | 7宫 | 婚姻过度理想化 → 反伤 |
| Saturn | 8宫 | 寿命/变故 |
| Jupiter | 9宫 | 信仰过度 → 教条 |
| Sun/Mercury | 10宫 | 事业/名声 |
| Jupiter | 11宫 | 收益 |
| Saturn | 12宫 | 损失/隔离 |

---

### P13. Argala (旁路耦合) - 信号补偿协议

- 激励源 (Argala)：目标顺数 +2 (资源输入), +4 (硬件地基), +11 (需求拉动)。
- 阻断源 (Virodha)：目标顺数 +12, +10, +3。
- 触发条件：目标位 [SAV < 25] 或 [司机 = 死/老/婴]。
- **强度计算：** ΣStrength = 各 Argala/Virodha 位置的行星数量 × 各自 Shadbala 百分比。空宫 = 0 贡献。
- 若 ΣStrength(Argala) > ΣStrength(Virodha)，激活旁路通路 (Bypass)。
- 若阻断源强度占优，执行相位抵消 (Phase Cancellation)，旁路失效。

---

## 解析完成后

输出所有已识别参数，并明确告知：
1. 哪些参数已成功提取
2. 哪些参数无法从 PDF 中识别（需要用户手动输入）
3. SAV 校验和是否 = 337

---

## OUTPUT: P1-P13 参数卡

对每颗行星（Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu）输出：

```
=== P1-P13 参数卡 ===

[行星名]:
  P1  身份: [Loyalist/Trader/Hostile] (掌管 X/Y 宫)
  P2  健康: [正常/燃烧/战争/逆行] (详情)
  P3  仓库: [掌管宫位性质] [合相星: ...]
  P4  库存SAV: [掌管宫位SAV值]
  P5  路段: [落入X宫] [Kendra/Trikona/Upachaya/凶路]
  P6  路况SAV: [落入宫位SAV值]
  P7  车型: [入旺/MT/入庙/友/中/敌/落陷] ([星座] [度数])
  P8  司机: [Yuva/Kumara/Baala/Vriddha/Mrita]
  P9  功率: Shadbala=[X] (阈值=[Y]) | Ishta=[A] Kashta=[B]
  P10 相位: [被谁看: 吉星/凶星相位列表]
  P11 星宿: [Nakshatra名] [Pada X] [星宿主=?] [Gana/Guna]
  P12 格局: [参与的Yoga列表]
  P13 旁路: [Argala/Virodha 状态]

...（9颗星逐一列出）

SAV 校验和: [X] (应=337)
Moon Nakshatra: [名称] → Dasha 起始星: [行星]
```

**等待用户确认后，方可进入 Phase 2。**

---

## Gate Check

```
ASSERT P1: 7星 + Rahu/Ketu 全部判定身份（共9项）
ASSERT P1: Sutra 7 已对每个吉星管 Kendra 的情况执行
ASSERT P1: Sutra 13 已标注 Rahu/Ketu 代理身份
ASSERT P2: 燃烧检查覆盖 5 颗星
ASSERT P2: 行星战争检查
ASSERT P2: 逆行标注
ASSERT P4: SAV 校验和 = 337
ASSERT P7: 7 星尊贵度全判定
ASSERT P8: 7 星 Avastha 全计算（含奇偶座正逆序）
ASSERT P9: 7 星 Shadbala vs 最低阈值逐项对比
ASSERT P9: Ishta/Kashta 全部提取
ASSERT P11: Moon Nakshatra 已确认
ASSERT 用户已确认参数
```
