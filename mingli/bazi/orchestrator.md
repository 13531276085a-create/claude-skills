# 八字分析编排器（Orchestrator）

> 基于 OpenAI/Anthropic/LangChain 三视角设计
> 替代原来的"一次性加载全部 harness"模式

---

## 设计原则

1. **看不到=不存在**（OpenAI）：每个 Phase 只加载当前 Phase 的 harness，不预加载
2. **独立评估者**（Anthropic）：Phase 完成后有机械校验，不靠 self-evaluation
3. **Reasoning Sandwich**（LangChain）：机械步骤降档，关键判断升档
4. **卡片即接口**：每个 Phase 的输出卡片是下一个 Phase 的唯一输入，无需回看原始数据

---

## Phase 路由表（100行索引，不是百科全书）

| Phase | 名称 | Harness 文件 | 推理强度 | 输出卡片 | 机械校验 |
|-------|------|-------------|---------|---------|---------|
| 0 | 排盘准备 | `phase0-harness.md` | 🟢轻（查表填空） | 排盘数据卡 | 干支阴阳匹配 |
| 1 | 宏观初览 | `phase1-harness.md` | 🟢轻（扫描标记） | 初览标记卡 | 6对地支已检查 |
| 2 | 核心定位 | `phase2-harness.md` | 🔴重（旺衰+格局） | 核心定位卡 | 旺衰六步+取格五步 |
| 3 | 用神体系 | `phase3-harness.md` | 🔴重（综合判断） | 用神体系卡 | 五神全标+病药全评 |
| 4 | 四柱逐柱 | `phase4-harness.md` | 🟡中（逐柱分析） | 四柱细读卡 | 四柱每柱已分析 |
| 5 | 地支扫描 | `phase5-harness.md` | 🟢轻（查表扫描） | 地支关系卡 | 10项检查完成 |
| 6 | 专项断事 | `phase6-harness.md` | 🟡中（专项推断） | 专项断事卡 | 每专项步骤完整 |
| 7 | 大运流年 | `phase7-harness.md` | 🟡中（动态分析） | 大运流年卡 | 每步运已分析 |
| 8 | 综合评判 | `phase8-harness.md` | 🔴重（交叉验证） | 最终报告 | 四维交叉已做 |

---

## 执行流程

```
用户输入排盘数据
    │
    ▼
┌─────────────────────────────────────────┐
│ Phase N 执行循环                          │
│                                          │
│  1. Read(`phaseN-harness.md`)  ← 按需加载 │
│  2. 读取前序卡片数据（上下文传递）          │
│  3. 按 harness 指令逐步执行               │
│  4. 输出本 Phase 卡片                     │
│  5. 机械校验（Gate Check）                │
│     ├── 通过 → 进入 Phase N+1            │
│     └── 不通过 → 标注缺失项，补做后重检   │
│                                          │
│  ★ 推理强度按路由表调节                    │
│  ★ 每个 Phase 的卡片写入 trace log        │
└─────────────────────────────────────────┘
    │
    ▼ (Phase 8 完成)
    │
┌─────────────────────────────────────────┐
│ 独立评估者（Evaluator）                   │
│                                          │
│  输入：Phase 0-8 的全部卡片               │
│  检查：                                   │
│  □ 旺衰判定与格局判定是否自洽             │
│  □ 用神是否与格局/调候一致                │
│  □ 专项断事是否引用了前序结论             │
│  □ 大运分析是否覆盖关键年龄段             │
│  □ 最终报告是否回答了命主的具体问题        │
│  □ 有无逻辑矛盾（如身弱却说财运极好）     │
│                                          │
│  输出：评估报告（通过/需修正 + 修正建议）  │
└─────────────────────────────────────────┘
    │
    ▼
  最终交付
```

---

## Gate Check（机械校验规则）

Gate Check 不是 self-evaluation，是**结构化检查**——检查输出卡片的字段是否完整，不判断内容对错。

### Phase 0 Gate
```
ASSERT 四柱干支 != null（4组）
ASSERT 十神标注 != null（4个天干）
ASSERT 藏干标注 != null（4个地支）
ASSERT 空亡 != null
ASSERT 大运列表.length >= 6
```

### Phase 1 Gate
```
ASSERT 地支关系检查.pairs == 6（6对全检查）
ASSERT 五行统计.sum == 8（4天干+4地支本气）
ASSERT 气候判定 != null
ASSERT 待验证问题.length >= 1
```

### Phase 2 Gate
```
ASSERT 旺衰.月令判定 IN [得令, 失令]
ASSERT 旺衰.日支判定 IN [得地, 失地]
ASSERT 旺衰.综合判定 IN [极强, 偏强, 中和偏强, 中和偏弱, 偏弱, 极弱, 从格]
ASSERT 格局名称 != null
ASSERT 格局成败 IN [成格, 破格, 成中有败]
ASSERT 调候满足度 IN [充分满足, 部分满足, 不满足]
ASSERT Phase1待验证问题.每项已回答
```

### Phase 3 Gate
```
ASSERT 用神 != null
ASSERT 喜神 != null
ASSERT 忌神 != null
ASSERT 病 != null OR 标注"无明显病"
ASSERT 十神组合.检查数 >= 3
```

### Phase 4 Gate
```
ASSERT 年柱分析 != null
ASSERT 月柱分析 != null
ASSERT 日柱分析 != null（含配偶宫）
ASSERT 时柱分析 != null
```

### Phase 5 Gate
```
ASSERT 检查项数 >= 8（六合/三合/三会/六冲/三刑/六害/空亡/墓库至少8项）
```

### Phase 6 Gate
```
ASSERT 至少完成1个专项分析
IF 命主有具体问题 THEN 对应专项必须完成
```

### Phase 7 Gate
```
ASSERT 大运分析.步数 >= 4（至少分析4步大运）
ASSERT 关键流年标记.count >= 3
```

### Phase 8 Gate
```
ASSERT 四维交叉验证矩阵 != null
ASSERT 确定性标注.count >= 3（强/弱/矛盾信号各至少标注）
ASSERT 禁止项未触发（无极端断语、无跳步）
```

---

## Trace Log（执行追踪）

每个 Phase 完成后，追加一条 trace 到内存中：

```json
{
  "phase": 2,
  "input_tokens_est": 1200,
  "output_tokens_est": 800,
  "gate_check": "PASS",
  "reasoning_level": "heavy",
  "key_decisions": ["旺衰=中和偏弱", "格局=偏印格(杀印相生)", "调候=部分满足"],
  "confidence": "high",
  "issues": []
}
```

用途：
1. 每次分析后追加到 traces/bazi-trace-log.md（持久化）
2. 积累10+案例后可批量分析失败模式
3. 用于 harness 迭代改进（LangChain boosting 方法论）

---

## Reasoning Sandwich 实现

| 推理强度 | 含义 | 适用 Phase | 执行方式 |
|---------|------|-----------|---------|
| 🟢 轻 | 查表填空，机械操作 | 0, 1, 5 | 严格按表操作，不需要推理 |
| 🟡 中 | 有限推理+模式匹配 | 4, 6, 7 | 按模板分析，允许适度推断 |
| 🔴 重 | 深度推理+综合判断 | 2, 3, 8 | 需要权衡多个维度，允许详细论证 |

实现方式：在每个 Phase harness 的开头标注推理强度，提示 AI 调节输出密度：
- 🟢：输出简洁，主要是表格和标记
- 🟡：输出中等，表格+简短分析
- 🔴：输出详细，允许展开论证

---

## 独立评估者 Prompt（Evaluator）

```
你是八字分析质量评估者。你的任务是审查一份八字分析报告，检查逻辑一致性和完整性。

你不做分析，只做评估。检查以下 7 项：

1. 内部一致性：旺衰判定 ↔ 格局判定 ↔ 用神选择 是否自洽？
   （如：判定身弱用印，但格局却取食伤为用 → 矛盾）

2. 调候一致性：调候满足度 ↔ 专项断事 是否一致？
   （如：调候不满足却说"一生安乐" → 矛盾）

3. 引用链完整：专项断事是否引用了 Phase 2-3 的核心结论？
   （如：事业分析没有提到格局 → 断裂）

4. 大运覆盖度：是否分析了命主当前所在的大运？
   （如：命主25岁，但大运分析从34岁开始 → 遗漏）

5. 问题回应度：命主的具体问题是否在报告中得到直接回答？
   （如：命主问"什么时候结婚"，报告只说"婚姻尚可" → 未回答）

6. 禁止项检查：
   - 有无极端断语？
   - 有无跳步（Phase 号不连续）？
   - 有无自相矛盾？

7. 信号强度：关键结论是否标注了确定性等级？

输出格式：
- 通过项：✅ [项目]
- 需修正：❌ [项目] — [具体问题] — [修正建议]
- 整体评级：A(优秀)/B(合格)/C(需修正)/D(重做)
```

---

## 与现有系统的集成点

| 改动 | 文件 | 做什么 |
|------|------|--------|
| Skill 入口 | `SKILL.md` | 八字模式执行时按 orchestrator 流程走 |
| Prompt | `bazi-prompt.md` | 精简为路由索引（不再内嵌百科），指向 orchestrator |
| Harness | `phase0-8-harness.md` | 每个文件开头加推理强度标签和 Gate Check 规则 |
| 评估者 | 新增 `bazi-evaluator.md` | 独立评估 prompt |
| Trace | 分析完成后追加到 `Obsidian/命理/traces/bazi-trace-log.md` | 持久化落盘，用于 LangChain boosting 迭代 |
