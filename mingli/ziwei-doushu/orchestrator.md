# 紫微斗数分析编排器（Orchestrator）

> 基于 OpenAI/Anthropic/LangChain 三视角设计
> 替代原来的"一次性加载全部 prompt"模式

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
| 0 | 排盘预检 | `ziwei-phase0-harness.md` | 🟢轻（数据提取+校验） | 排盘数据卡 | 干支配对+真太阳时+数据完整性 |
| 1 | 命盘总论 | `ziwei-phase1-harness.md` | 🟡中（格局判定） | 命盘总论卡 | 格局+四化落宫+来因宫全标注 |
| 2 | 飞星四化全景 | `ziwei-phase2-harness.md` | 🔴重（飞化网络分析） | 飞化全景卡 | 12宫飞化表完整+闭环标注 |
| 3 | 十二宫逐宫 | `ziwei-phase3-harness.md` | 🟡中（逐宫分析） | 十二宫卡 | 12宫全覆盖+每宫飞化溯源 |
| 4 | 主题专项 | `ziwei-phase4-harness.md` | 🟡中（专项推断） | 专项断事卡 | 每结论附飞化依据+立极标注 |
| 5 | 大限流年 | `ziwei-phase5-harness.md` | 🔴重（三盘叠合） | 大限流年卡 | 前6限已分析+关键流年>=5 |
| 6 | 综合评判 | `ziwei-phase6-harness.md` | 🔴重（交叉验证） | 最终报告 | 时间线+建议+确定性标注 |

---

## 执行流程

```
用户输入排盘数据（或排盘截图）
    |
    v
+-------------------------------------------+
| Phase N 执行循环                            |
|                                            |
|  1. Read(`ziwei-phaseN-harness.md`) <- 按需 |
|  2. 读取前序卡片数据（上下文传递）             |
|  3. 按 harness 指令逐步执行                  |
|  4. 输出本 Phase 卡片                        |
|  5. 机械校验（Gate Check）                   |
|     +-- 通过 -> 进入 Phase N+1              |
|     +-- 不通过 -> 标注缺失项，补做后重检      |
|                                            |
|  * 推理强度按路由表调节                       |
|  * 每个 Phase 的卡片写入 trace log           |
|                                            |
|  [回溯触发检查]                              |
|     Phase 4 -> Phase 2: 飞化全景有遗漏       |
|     Phase 5 -> Phase 1: 格局判定需修正       |
+-------------------------------------------+
    |
    v (Phase 6 完成)
    |
+-------------------------------------------+
| 独立评估者（Evaluator）                      |
|                                            |
|  输入：Phase 0-6 的全部卡片                  |
|  检查：                                     |
|  [ ] 格局判定与飞化全景是否自洽               |
|  [ ] 飞化路径在逐宫分析中是否全部溯源         |
|  [ ] 专项断事是否引用了飞化依据               |
|  [ ] 大限分析是否覆盖关键年龄段               |
|  [ ] 三盘叠合逻辑是否正确                    |
|  [ ] 最终报告是否回答了命主的具体问题          |
|  [ ] 有无逻辑矛盾或极端断语                  |
|                                            |
|  详见 -> ziwei-evaluator.md                 |
|  输出：评估报告（通过/需修正 + 修正建议）      |
+-------------------------------------------+
    |
    v
  最终交付
```

---

## Gate Check（机械校验规则）

Gate Check 不是 self-evaluation，是**结构化检查**——检查输出卡片的字段是否完整，不判断内容对错。

### Phase 0 Gate
```
ASSERT 基本信息.性别 != null
ASSERT 基本信息.农历时间 != null
ASSERT 基本信息.真太阳时校验 IN [已校验, 无需校验, 待确认]
ASSERT 命宫位置 != null
ASSERT 身宫位置 != null
ASSERT 五行局 != null
ASSERT 十二宫.count == 12
ASSERT 每宫.主星 != null OR 标注"空宫借对宫"
ASSERT 生年四化.count == 4
ASSERT 数据来源 IN [文墨天机, iztro, 其他排盘工具, 手工输入]
```

### Phase 1 Gate
```
ASSERT 命宫主星格局 != null
ASSERT 格局类型 != null
ASSERT 身宫位置分析 != null
ASSERT 来因宫分析 != null
ASSERT 生年四化.每颗已分析
ASSERT 四化格局判定 != null
ASSERT 特殊格局清单.checked == true
ASSERT 五行局影响 != null
```

### Phase 2 Gate
```
ASSERT 飞化路径表.宫数 == 12
ASSERT 每宫.四化路径 == 4
ASSERT 飞化溯源.每个上行标记已溯源
ASSERT 飞化溯源.每个下行标记已说明
ASSERT 飞化分类.四类全标注
ASSERT 忌转忌链.已追踪 == true
ASSERT 两宫循环忌.已检查 == true
ASSERT Phase1待深入问题.每项已回答
```

### Phase 3 Gate
```
ASSERT 已分析宫数 == 12
ASSERT 每宫.主星含义 != null
ASSERT 每宫.辅星影响 != null
ASSERT 每宫.飞化入溯源 != null OR "无飞化入"
ASSERT 每宫.飞化出说明 != null OR "无飞化出"
ASSERT 每宫.潜在问题 != null OR "无明显问题"
```

### Phase 4 Gate
```
ASSERT 已分析专项数 >= 4
ASSERT 每专项.核心宫位 != null
ASSERT 每专项.飞化佐证 != null
ASSERT 每专项.动态立极 != null
ASSERT 无孤证
```

### Phase 5 Gate
```
ASSERT 大限分析.步数 >= 6
ASSERT 每步大限.宫位+主星+四化 != null
ASSERT 关键流年.count >= 5
ASSERT 每关键流年.三盘叠合 != null
ASSERT 流年命宫推算.方法已标注
```

### Phase 6 Gate
```
ASSERT 关键事件时间线.count >= 8
ASSERT 每事件.飞化依据 != null
ASSERT 核心优势.count >= 2
ASSERT 核心短板.count >= 1
ASSERT 阶段策略表.大限数 >= 4
ASSERT 确定性标注.count >= 5
ASSERT 无极端断语
ASSERT 无骑墙判断
```

---

## 回溯触发条件

回溯是紫微编排器特有的机制。飞化网络的复杂性意味着后续 Phase 可能发现前序分析的遗漏。回溯不是失败，是系统自我修正。

```
回溯路径 1: Phase 4 -> Phase 2
  触发条件: 专项断事发现飞化全景有遗漏或错误
  判定方式: Phase 4 分析中引用的飞化路径在 Phase 2 卡片中不存在
  执行: 重跑 Phase 2，补全遗漏路径，然后从 Phase 3 重新推进
  上限: 1 次

回溯路径 2: Phase 5 -> Phase 1
  触发条件: 大限分析发现格局判定可能有误
  判定方式: 大限四化与原局格局产生不可调和的矛盾
  执行: 重跑 Phase 1，修正格局判定，然后从 Phase 2 重新推进
  上限: 1 次
```

回溯触发后，trace log 记录 `"backtrack": true` 和回溯原因。

---

## Trace Log（执行追踪）

每个 Phase 完成后，追加一条 trace 到内存中：

```json
{
  "phase": 2,
  "input_tokens_est": 1500,
  "output_tokens_est": 1200,
  "gate_check": "PASS",
  "reasoning_level": "heavy",
  "key_decisions": ["格局=紫杀在巳(将星得地)", "飞化闭环=命迁线禄权交驰"],
  "confidence": "high",
  "backtrack": false,
  "issues": []
}
```

用途：
1. 每次分析后追加到 traces/ziwei-trace-log.md（持久化）
2. 积累 10+ 案例后可批量分析失败模式
3. 用于 harness 迭代改进（LangChain boosting 方法论）

### Trace 落盘（程序化）

每个 Phase 完成后，执行：
```bash
python3 ~/.claude/skills/mingli/scripts/trace-writer.py \
  --name "[命主标识]" \
  --phase [N] \
  --gate-result "[PASS/FAIL]" \
  --reasoning-level "[light/medium/heavy]" \
  --key-decisions "[逗号分隔的关键决策]" \
  --confidence "[high/medium/low]" \
  --issues "[逗号分隔的问题]" \
  --backtrack "[回溯目标Phase或空]"
```

Gate Check 程序化校验：
```bash
python3 ~/.claude/skills/mingli/scripts/gate-check.py [phase] [card_file]
```
先运行程序化校验（结构检查），再让 AI 做内容检查。两者都通过才算 Gate Check PASS。

---

## Reasoning Sandwich 实现

| 推理强度 | 含义 | 适用 Phase | 执行方式 |
|---------|------|-----------|---------|
| 🟢 轻 | 数据提取+校验，机械操作 | 0 | 严格按表操作，不需要推理 |
| 🟡 中 | 有限推理+模式匹配 | 1, 3, 4 | 按模板分析，允许适度推断 |
| 🔴 重 | 深度推理+综合判断 | 2, 5, 6 | 需要权衡多个维度，允许详细论证 |

实现方式：在每个 Phase harness 的开头标注推理强度，提示 AI 调节输出密度：
- 🟢：输出简洁，主要是表格和标记
- 🟡：输出中等，表格+简短分析
- 🔴：输出详细，允许展开论证

---

## 独立评估者 Prompt（Evaluator）

详见 `ziwei-evaluator.md`。评估者检查 9 项：

1. 内部一致性：格局判定 <-> 飞化全景 <-> 逐宫分析 是否自洽
2. 飞化完整性：12 宫飞化路径是否全部溯源，无遗漏
3. 引用链完整：专项断事是否引用了 Phase 1-3 的核心结论
4. 大限覆盖度：是否分析了命主当前所在的大限
5. 三盘叠合正确性：原局/大限/流年叠合逻辑是否正确
6. 问题回应度：命主的具体问题是否在报告中得到直接回答
7. 飞化闭环验证：发现的闭环是否在专项/大限中被引用
8. 禁止项检查：无极端断语、无跳步、无自相矛盾
9. 信号强度：关键结论是否标注了确定性等级

---

## 与现有系统的集成点

| 改动 | 文件 | 做什么 |
|------|------|--------|
| Skill 入口 | `SKILL.md` | 紫微模式执行时按 orchestrator 流程走 |
| Prompt | `ziwei-prompt.md` | 精简为路由索引（不再内嵌百科），指向 orchestrator |
| Harness | `ziwei-phase0-6-harness.md` | 每个文件开头加推理强度标签和 Gate Check 规则 |
| 评估者 | 新增 `ziwei-evaluator.md` | 独立评估 prompt（9 项检查） |
| Trace | 执行时内存追踪 | 追加到 traces/ziwei-trace-log.md |
