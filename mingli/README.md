# mingli-skills — AI 命理工程化

> 让大语言模型精确理解和应用中国传统命理体系，而非靠幻觉"算命"。

## 这是什么

一套工程化的命理分析 Skill 系统，专为 Claude Code / LLM Agent 设计。包含 **5 大命理体系** + **跨体系交叉验证框架**，��计 114 个文件，约 1.4MB 方法论 + 排盘引擎。

核心理念：**LLM 做推理解读，确定性计算交给脚本，每个结论可追溯、可验证。**

## 体系一览

| 体系 | 文件数 | 阶段数 | 独立评估者 | 说明 |
|------|--------|--------|-----------|------|
| [紫微斗数](ziwei-doushu/) | 13 | 7 Phase | 9 项检查 | 飞星四化全景 + 大限流年推演 |
| [八字](bazi/) | 27 | 8 Phase + 12 Step 大运 | 7 项检查 | 四维交叉验证（旺衰/格局/调候/病药）|
| [六爻](liuyao/) | 12 | 8 Phase | 6 项检查 | 用神-旺衰-生克-吉凶-应期全链路 |
| [印占/吠陀](yinzhan/) | 14 | 12 Phase | 6 项检查 | Parashari + KP + Jaimini 多学派 |
| [奇门遁甲](qimen-dunjia/) | 45 | 9 Step 断卦 | GAN 独立复核 | Python 排盘引擎 + 17 JSON + 12 份调研 |
| [共享模块](shared/) | 5 | — | — | 多派系引擎 + 合婚 SOP + 质量脚本 |

## 架构

```
SKILL.md                        # 顶层入口（单维度 / 多维度两种模式）
│
├── ziwei-doushu/               # 紫微斗数 — 7 Phase SOP
│   ├── orchestrator.md         #   编排器：阶段调度 + Gate Check
│   ├── evaluator.md            #   独立评估者：9 项质量检查
│   ├── prompt.md               #   核心 prompt
│   └── references/             #   Phase 0-6 harness + 72KB 基础知识库
│       ├── basics.md           #     十四主星 + 十二宫 + 辅星 + 神煞全解
│       ├── phase0-harness.md   #     排盘预检（真太阳时 + 夏令时 + 数据完整性）
│       ├── phase1-harness.md   #     命盘总论（格局 + 身宫 + 来因宫 + 四化格局）
│       ├── phase2-harness.md   #     飞星四化全景（12宫飞化表 + 循环忌 + 闭环）
│       ├── phase3-harness.md   #     十二宫逐宫（每宫 7 层分析）
│       ├── phase4-harness.md   #     主题专项（性格/事业/财运/婚姻/健康/学业/置产）
│       ├── phase5-harness.md   #     大限流年（前 6 限必析 + 关键流年 >= 5）
│       ├── phase5-v2-harness.md#     大限流年增强版
│       ├── phase6-harness.md   #     综合评判（时间线 + 建议 + 确定性标注）
│       └── flow-year-harness.md#     流年专项
│
├── bazi/                       # 八字 — 8 Phase + 12 Step 大运
│   ├── orchestrator.md         #   编排器
│   ├── evaluator.md            #   独立评估者
│   ├── prompt.md               #   四维交叉验证框架
│   ├── references/             #   Phase 0-8 harness
│   │   ├── phase0-harness.md   #     排盘准备（四柱/十神/藏干/空亡）
│   │   ├── phase1-harness.md   #     宏观初览（地支关系 6 对全检）
│   │   ├── phase2-harness.md   #     核心定位（旺衰 + 格局 + 调候）
│   │   ├── phase3-harness.md   #     用神体系（五神 + 病药 + 组合）
│   │   ├── phase4-harness.md   #     四柱逐柱
│   │   ├── phase5-harness.md   #     地支扫描（10 项检查）
│   │   ├── phase6-harness.md   #     专项断事（事业/财运/婚姻/健康）
│   │   ├── phase7-harness.md   #     大运流年入口
│   │   ├── phase8-harness.md   #     综合评判（四维交叉 + A/B/C/D 评级）
│   │   ├── sop-research.md     #     SOP 设计调研报告
│   │   └── test-cases.md       #     测试案例集
│   └── dayun/                  #   大运流年子系统（12 Step，250+ 规则）
│       ├── orchestrator.md     #     12 步编排器
│       ├── step0-harness.md    #     前序数据提取
│       ├── step1-harness.md    #     命局力量量化
│       ├── step2-harness.md    #     干支动态作用
│       ├── step3-harness.md    #     旺衰定级校验
│       ├── step4-harness.md    #     格局调候校验
│       ├── step5-harness.md    #     原局信号扫描
│       ├── step6-harness.md    #     逐步大运分析（核心，44KB）
│       ├── step7-harness.md    #     关键流年筛选
│       ├── step8-harness.md    #     断事信号匹配
│       ├── step9-harness.md    #     应期定位
│       ├── step10-harness.md   #     古籍交叉验证
│       └── step11-harness.md   #     综合输出 + 校验清单
│
├── liuyao/                     # 六爻 — 8 Phase SOP
│   ├── orchestrator.md         #   编排器
│   ├── evaluator.md            #   独立评估者
│   ├── prompts.md              #   核心 prompt
│   ├── v2-prompt.md            #   V2 增强 prompt
│   └── references/             #   Phase 0-7 harness
│       ├── phase0-harness.md   #     读盘提取（字段完整性）
│       ├── phase1-harness.md   #     验盘定位（问事类型 + 特殊卦象）
│       ├── phase2-harness.md   #     取用神（四神全标 + 伏神）
│       ├── phase3-harness.md   #     审旺衰（月破空亡全查）
│       ├── phase4-harness.md   #     析生克（动爻 + 世应 + 伏飞）
│       ├── phase5-harness.md   #     断吉凶（明确判断 + 分类专项）
│       ├── phase6-harness.md   #     推应期（病药流程 + 双格式）
│       └── phase7-harness.md   #     综合报告
│
├── yinzhan/                    # 印占/吠陀 — 12 Phase SOP
│   ├── orchestrator.md         #   编排器（Parashari + KP + Jaimini）
│   ├── evaluator.md            #   独立评估者
│   └── references/             #   Phase 0-11 harness
│       ├── phase0-harness.md   #     Lagna 验证（±10min + Ayanamsa）
│       ├── phase1-harness.md   #     参数提取（P1-P13 全标 + SAV=337）
│       ├── phase2-harness.md   #     Model A 模式（9 星归 5 种模式）
│       ├── phase3-harness.md   #     Model B 表现力（Ishta/Kashta）
│       ├── phase4-harness.md   #     Model C 影响力
│       ├── phase5-harness.md   #     D9 校准（Jaimini）
│       ├── phase6-harness.md   #     宫位诊断（管理者/租客/硬件三层）
│       ├── phase7-harness.md   #     Dasha 时间轴
│       ├── phase8-harness.md   #     Transit 过境
│       ├── phase9-harness.md   #     收敛验证（每主题 >= 2 信号）
│       ├── phase10-harness.md  #     KP 精确定时 [可选]
│       └── phase11-harness.md  #     化解建议 [可选]
│
├── qimen-dunjia/               # 奇门遁甲 — Python 引擎 + 断卦 SOP
│   ├── SKILL.md                #   排盘引擎 skill
│   ├── duanjua-skill.md        #   断卦解读 skill（9 步 SOP）
│   ├── ARCHITECTURE.md         #   三层架构说明
│   ├── KNOWN_ISSUES.md         #   已知坑 + 防线
│   ├── scripts/                #   Python 排盘引擎
│   │   ├── qimen.py            #     核心排盘（sxtwl 库 + 9 步算法）
│   │   ├── verify.py           #     144 项断言验证
│   │   ├── trace.py            #     推理链追踪
│   │   └── analyze_traces.py   #     失败模式分析
│   ├── data/                   #   17 个 JSON 数据文件
│   │   ├── dipan_18ju.json     #     18 局地盘排布
│   │   ├── shigan_keying_81.json #   81 组十干克应格局
│   │   ├── duanjua_knowledge.json #  断卦知识库（用神/吉凶/生克）
│   │   └── ...                 #     五行/空亡/击刑/入墓/门迫等
│   └── research/               #   12 份深度调研报告
│
└── shared/                     # 共享模块
    ├── multi-school-engine.md  #   多派系引擎
    ├── hehun-sop.md            #   合婚 SOP
    └── scripts/                #   质量保证工具
        ├── gate-check.py       #     Gate Check 机械校验
        ├── trace-analyzer.py   #     Trace 日志分析
        └── trace-writer.py     #     Trace 日志写入
```

## 核心设计原则

### 1. 多阶段 SOP + Gate Check

每个体系拆解为多个 Phase，每个 Phase 完成后执行机械校验（不判断内容对错，只检查字段完整性）：

```
Phase N 完成 → Gate Check → PASS → Phase N+1
                          → FAIL → 标注缺失项 → 补做 → 重检
```

推理强度分三级，防止 LLM 在简单步骤上过度推理或在复杂步骤上偷懒。

### 2. 独立评估者

每个体系都有独立评估者，在分析完成后从原始数据出发独立推导，找出解读中的矛盾和遗漏。这不是 self-evaluation，而是对抗性验证（类似 GAN 的判别器）。

### 3. 飞星四化全景（紫微专有）

不只是看生年四化落哪个宫，而是追踪所有 12 宫的宫干飞化路径：

- 12 宫 × 4 化 = 48 条飞化路径
- 循环忌检测（A 忌入 B，B 忌入 A）
- 高危线标注（忌冲对宫的传导链）
- 闭环分析（忌出冲回自身）

### 4. 四维交叉验证（八字专有）

八字分析不靠单一方法论下结论，而是四个维度独立判断后交叉：

| 维度 | 方法 | 回答什么 |
|------|------|---------|
| 旺衰法 | 日主在月令的生克 | 能量厚度 |
| 格局法 | 月令本气透干 | 社会定位 |
| 调候法 | 冬冷夏热平衡 | 舒适度 |
| 病药法 | 最大病有无药克 | 危机化解力 |

四维互动关系 > 简单叠加。

### 5. 多维度综合分析（跨体系）

当多个体系同时可用时，五步流程：

1. **各体系独立完整分析**
2. **大运/行运三维对照表**（紫微大限 × 八字大运 × 印占 Dasha）
3. **交叉验证矩阵**（强一致/中一致/弱一致/矛盾）
4. **逐步推理与质疑检验**（矛盾信号展开调和分析）
5. **量化趋势曲线图**（matplotlib，4 条线叠加）

### 6. 信号强度标注

所有结论必须标注置信度：

- **强信号** ✅：>= 3 个维度指向相同方向
- **弱信号** ⚠️：2 个维度指向相同 或 1 个维度有力度证据
- **矛盾信号** ❌：维度指向相反，需展开调和分析

## 禁止项

- 使用极端断语（"必定大富大贵"、"一生悲惨"）
- 跳步分析（Phase 号不连续）
- 孤证定论（单一信号作为确定性判断）
- 凶象不转译（必须转化为风险与课题，而非宿命论断）
- 模糊不标来源（"可能"、"也许"必须附置信度）

## 使用方式

### 在 Claude Code 中

```bash
# 完整系统
cp -r . ~/.claude/skills/mingli/

# 单个体系（如紫微斗数）
mkdir -p ~/.claude/skills/ziwei-doushu
cp -r ziwei-doushu/* ~/.claude/skills/ziwei-doushu/
```

### 作为 LLM Prompt 参考

每个体系的 `orchestrator.md` 是最佳入口，定义了完整的分析流程、阶段调度和质量标准。

## 统计

| 指标 | 数值 |
|------|------|
| Markdown 文件 | 93 |
| Python 脚本 | 7 |
| JSON 数据 | 17 |
| 总文件数 | 114 |
| 总体积 | ~1.4MB |
| 紫微斗数基础库 | 72KB（十四主星全解） |
| 八字大运 Step 6 | 44KB（核心评分公式） |
| 奇门排盘引擎 | 9 步算法 + 144 项验证 |
| 调研报告 | 12 份 + 250 条规则 + 1500 量化数值 |

## License

MIT
