# 六爻解卦编排器（Orchestrator）

> 基于 60+ 网页 + 5 部经典著作交叉验证
> 架构参照八字 SOP harness 模式（卡片即接口 + Gate Check + Trace Log）

---

## 设计原则

1. **看不到=不存在**：每个 Phase 只加载当前 Phase 的 harness，不预加载
2. **独立评估者**：Phase 7 完成后有独立交叉验证，不靠 self-evaluation
3. **Reasoning Sandwich**：机械步骤降档，关键判断升档
4. **卡片即接口**：每个 Phase 的输出卡片是下一个 Phase 的唯一输入
5. **五源验证**：每个规则节点至少 5 个可追溯来源

---

## Phase 路由表

| Phase | 名称 | Harness 文件 | 推理强度 | 输出卡片 | Gate Check |
|-------|------|-------------|---------|---------|------------|
| 0 | 读盘提取 | `liuyao-phase0-harness.md` | 🟢轻（读图填表） | 卦象数据卡 | 字段完整性校验 |
| 1 | 验盘定位 | `liuyao-phase1-harness.md` | 🟢轻（扫描标记） | 定位标记卡 | 验证通过+问事类型已确定 |
| 2 | 取用神 | `liuyao-phase2-harness.md` | 🔴重（路由决策） | 用神体系卡 | 四神全标+伏神已处理 |
| 3 | 审旺衰 | `liuyao-phase3-harness.md` | 🔴重（量化评估） | 旺衰评估卡 | 关键爻旺衰全标+特殊状态全查 |
| 4 | 析生克 | `liuyao-phase4-harness.md` | 🟡中（逐爻分析） | 生克关系卡 | 动爻全析+世应已论 |
| 5 | 断吉凶 | `liuyao-phase5-harness.md` | 🔴重（综合判断） | 吉凶判断卡 | 明确判断+分类专项+引用前序 |
| 6 | 推应期 | `liuyao-phase6-harness.md` | 🟡中（病药推断） | 应期推断卡 | 应期有依据+双格式标注 |
| 7 | 综合报告 | `liuyao-phase7-harness.md` | 🟡中（交叉验证） | 最终解卦报告 | 一致性检查通过 |

---

## 执行流程

```
用户提供排盘截图 + 问事
    │
    ▼
┌─────────────────────────────────────────┐
│ Phase N 执行循环                          │
│                                          │
│  1. Read(`liuyao-phaseN-harness.md`)     │
│  2. 读取前序卡片数据                      │
│  3. 按 harness 指令逐步执行               │
│  4. 输出本 Phase 卡片                     │
│  5. Gate Check（机械校验）                │
│     ├── PASS → Phase N+1                │
│     └── FAIL → 标注缺失项，补做后重检     │
│                                          │
│  ★ 推理强度按路由表调节                    │
│  ★ 每个 Phase 的卡片写入 trace log        │
└─────────────────────────────────────────┘
    │
    ▼ (Phase 7 完成)
    │
┌─────────────────────────────────────────┐
│ 独立评估者（liuyao-evaluator.md）         │
│                                          │
│  输入：Phase 0-7 的全部卡片               │
│  检查：                                   │
│  □ 用神取用是否与问事类型匹配             │
│  □ 旺衰判断是否与月日一致                 │
│  □ 断吉凶是否引用了旺衰+生克结论          │
│  □ 应期推断是否与吉凶方向一致             │
│  □ 有无逻辑矛盾                          │
│  □ 是否直接回答了求测者的问题             │
│                                          │
│  输出：评估报告（通过/需修正 + 修正建议）  │
└─────────────────────────────────────────┘
    │
    ▼
  最终交付
```

---

## Gate Check 规则

Gate Check 是**结构化检查**——检查输出卡片的字段是否完整，不判断内容对错。

### Phase 0 Gate
```
ASSERT 日期干支 != null（年月日干支 + 旬空）
ASSERT 主卦名 != null
ASSERT 变卦名 != null OR 标注"纯静卦"
ASSERT 六爻数据.length == 6（每爻含：爻位/六亲/地支/六神/动静）
ASSERT 世爻位置 != null AND 应爻位置 != null
ASSERT 问事内容 != null
```

### Phase 1 Gate
```
ASSERT 问事类型 IN [财运, 婚姻, 事业, 疾病, 官司, 考试, 出行, 天气, 失物, 其他]
ASSERT 特殊卦象检查已完成（六冲/六合/游魂/归魂/反吟/伏吟）
ASSERT 持世爻六亲已标注
ASSERT 数据一致性校验 == PASS
```

### Phase 2 Gate
```
ASSERT 用神 != null（标明六亲+地支+爻位）
ASSERT 原神 != null
ASSERT 忌神 != null
ASSERT 仇神 != null
IF 用神两现 THEN 取舍理由已标注
IF 用神不上卦 THEN 伏神已处理（飞伏关系已标注）
```

### Phase 3 Gate
```
ASSERT 用神旺衰 IN [旺, 相, 休, 囚, 死]
ASSERT 月建对用神作用 != null
ASSERT 日辰对用神作用 != null
ASSERT 空亡检查.完成 == true
ASSERT 月破检查.完成 == true
ASSERT 原神旺衰 != null
ASSERT 忌神旺衰 != null
```

### Phase 4 Gate
```
ASSERT 每个动爻已分析（变爻关系+回头生克+进退神）
ASSERT 世应关系已论述
IF 暗动爻存在 THEN 已标注
IF 伏神存在 THEN 飞伏互作已分析
ASSERT 原神能否生用神.判断 != null
ASSERT 忌神能否克用神.判断 != null
```

### Phase 5 Gate
```
ASSERT 吉凶判断 IN [大吉, 吉, 小吉, 平, 小凶, 凶, 大凶]
ASSERT 判断依据.引用Phase数 >= 2（必须引用 Phase 3 和 Phase 4）
ASSERT 分类专项分析已完成（与问事类型匹配）
ASSERT 确定性标注 != null
```

### Phase 6 Gate
```
ASSERT 应期 != null
ASSERT 应期推理路径 != null（病→药→应期）
ASSERT 时间单位合理性已确认（近应/远应）
ASSERT 应期标注含干支和公历两种格式
```

### Phase 7 Gate
```
ASSERT 交叉验证矩阵 != null
ASSERT 矛盾检查 == PASS OR 矛盾已标注解释
ASSERT 最终回答直接回应了求测者的问题
ASSERT 确定性等级已标注（✅/⚠️/❌）
ASSERT 禁止项未触发（无极端断语/无跳步/无自相矛盾）
```

---

## Trace Log

每个 Phase 完成后追加一条 trace：

```json
{
  "type": "liuyao",
  "phase": 2,
  "gate_check": "PASS",
  "reasoning_level": "heavy",
  "key_decisions": ["用神=妻财午火(三爻)", "原神=子孙巳火", "忌神=兄弟寅木"],
  "confidence": "high",
  "issues": []
}
```

持久化到 `Obsidian/命理/traces/liuyao-trace-log.md`。

---

## 核心方法论共识（12+ 来源 100% 一致）

### 优先级链
```
回头生克 / 化进退 ＞ 动爻生克 ＞ 日月作用
内因（卦体）＞ 外因（日月），但外因可引发内因
用神 ＞ 世爻 ＞ 其他爻
月建（定旺衰）＞ 日辰（定具体生克）＞ 太岁（管大事）
```

### 速记口诀
> 一看空，二看冲，三看刑合衰旺中。
> 四看化出进退死，五看神煞凶不凶。
> 六看用爻之位置，七看伏神出牢笼。
> 八看反伏吟流泪，九看外应十观容。

### 经典著作权威性排序
《增删卜易》 > 《卜筮正宗》 > 《黄金策》 > 《易隐》 > 《易林补遗》

---

## 来源索引（总览）

详细来源追溯见各 Phase harness 文件。总体来源体系：

| 来源类型 | 数量 | 代表 |
|---------|------|------|
| 经典原文 | 3 | 增删卜易/卜筮正宗/黄金策（劝学网全文） |
| 知乎深度文 | 15 | p/521636345, p/562811848 等 |
| 专业易学网站 | 15 | 易阳子/易师汇/国易堂/六爻详真等 |
| 百科 | 2 | 百度百科/维基百科 |
| 现代著作 | 3 | 邵伟华/王虎应/六爻新大陆 |
