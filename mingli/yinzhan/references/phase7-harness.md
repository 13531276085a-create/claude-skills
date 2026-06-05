# Phase 7: Dasha 时间轴集成

> 推理强度：🔴重（时间集成）
> 输入：Phase 1 P11.5 (Moon Nakshatra) + Phase 6 宫位诊断卡
> 输出：Dasha 时间轴卡
> 下一步：Phase 8（连续执行）

---

**核心公式：** `Birth Chart (What) × Dasha (When) × Transit (Trigger) = Event`

此步骤将静态盘面分析接入时间轴，回答"什么时候发生"。

**数据入口：** 从 Phase 1 的 P11.5 获取 Moon Nakshatra → 查下表确定 Mahadasha 起始星。

## 7.1 Dasha 选择决策树

```
默认 → Vimshottari Dasha (120年周期，Moon Nakshatra 起算)
    ↓
交叉验证 #1 → Yogini Dasha (36年周期，快速断事，女性盘/健康/关系尤佳)
    ↓
交叉验证 #2 → Chara Dasha (Jaimini, Rashi-based)
    ↓
[若三者指向同一时段] → 高置信预测
[若分歧] → 标注不确定性，以 Vimshottari 为主
```

## 7.2 Vimshottari Dasha 时间表

| Planet | 年数 | Nakshatra 起始 |
|--------|------|---------------|
| Ketu | 7 | Ashwini, Magha, Moola |
| Venus | 20 | Bharani, P.Phalguni, P.Ashadha |
| Sun | 6 | Krittika, U.Phalguni, U.Ashadha |
| Moon | 10 | Rohini, Hasta, Shravana |
| Mars | 7 | Mrigashira, Chitra, Dhanishta |
| Rahu | 18 | Ardra, Swati, Shatabhisha |
| Jupiter | 16 | Punarvasu, Vishakha, P.Bhadrapada |
| Saturn | 19 | Pushya, Anuradha, U.Bhadrapada |
| Mercury | 17 | Ashlesha, Jyeshtha, Revati |

**层级：** Mahadasha (大运) → Antardasha (次运) → Pratyantardasha (细运)

## 7.3 Dasha 解读六步法

对每个 Mahadasha/Antardasha 组合：

1. **Dasha lord 的 P1-P13 参数** = 该时期的底色
2. **Dasha lord 掌管的宫位** = 被激活的人生领域
3. **Dasha lord 落入的宫位** = 事件发生的场景
4. **Dasha lord 在 D9 的状态** = 该时期成果的兑现质量
5. **Dasha lord 参与的 Yoga** = 潜伏格局是否在此期激活
6. **Mahadasha + Antardasha lord 的关系**:
   - 互为友好 + 吉宫距离(1/5/9) = 顺流期
   - 互为敌对 + 凶宫距离(6/8/12) = 逆流期

---

## OUTPUT: Dasha 时间轴卡

```
=== Dasha 时间轴 ===
出生至今: [列出已经历的 Mahadasha 及关键 Antardasha]
当前运势: [当前 Mahadasha/Antardasha] → 核心主题: [描述]
未来关键转折: [下一个重大 Dasha 切换时间及预测]

=== 关键时间窗口 ===
[时间段1]: [Dasha组合] → [预测事件/主题] | 置信度: [高/中/低]
[时间段2]: ...

=== Yogini Dasha 交叉验证 ===
Yogini 8阶周期表:
  Mangala(Moon)=1yr | Pingala(Sun)=2yr | Dhanya(Jupiter)=3yr | Bhramari(Mars)=4yr
  Bhadrika(Mercury)=5yr | Ulka(Saturn)=6yr | Siddha(Venus)=7yr | Sankata(Rahu)=8yr
当前 Yogini 期: [X]
[是否与 Vimshottari 指向一致？标注]
```

---

## Gate Check

```
ASSERT P11.5 Moon Nakshatra → Dasha 起始星桥梁已显式引用
ASSERT 当前 Mahadasha + Antardasha 已确认
ASSERT Dasha 六步法至少对当前 MD/AD 执行
ASSERT 格局激活条件已检查（哪些 Yoga 在当前 Dasha 被激活）
ASSERT Yogini Dasha 交叉验证已执行
```
