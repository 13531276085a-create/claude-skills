# Claude Code Skills 集合

15 个 Claude Code Agent Skills，涵盖思维框架、股票分析、视觉创作、视频处理、命理分析等领域。

---

## 思维框架类

### [mao-zedong-perspective](./mao-zedong-perspective/) —— 毛泽东思维方式
以毛泽东的思维方式思考和表达。基于《实践论》《矛盾论》《论持久战》《反对本本主义》提炼。穿透表象、抓住本质、做出明确判断。触发词：毛选思维、矛盾论视角、毛式分析。

### [sunyuchen-perspective](./sunyuchen-perspective/) —— 孙宇晨 × 幻夜梦屿 社会心理工具箱
注意力经济学、人格工程、受众心理操控、情绪去耦、激进实用主义。超过25个信息源深度调研。触发词：社会心理分析、人性洞察、注意力策略。

### [liangxiangrun-perspective](./liangxiangrun-perspective/) —— 梁湘润思维方式
（待补充描述）

---

## 股票投资类

### [mao-stock-analysis](./mao-stock-analysis/) —— 毛选精华思想 × 股票分析
将《实践论》《矛盾论》《论持久战》的唯物辩证法、矛盾分析法、持久战战略转化为结构化股票分析工具。触发词：毛选股票、矛盾论分析股票、持久战炒股。

---

## 视觉创作类

### [guizang-ppt-skill](./guizang-ppt-skill/) —— 归藏网页PPT
生成横向翻页网页PPT，含 WebGL 背景、章节幕封、数据大字报、图片网格。两种风格：电子杂志×电子墨水 / 瑞士国际主义。触发词：杂志风PPT、Swiss Style、horizontal swipe deck。

### [guizang-social-card-skill](./guizang-social-card-skill/) —— 归藏社交卡片
生成归藏风格小红书图文、微信公众号封面。3:4 竖版 + 21:9 横版 + 1:1 方形封面。触发词：小红书图文、Rednote、社交卡片。

### [frontend-slides](./frontend-slides/) —— 前端幻灯片
通过视觉探索而非抽象选择，创建动画丰富的 HTML 演示文稿，支持 PPT/PPTX 转换。

### [kami](./kami/) —— 排版引擎
专业文档和产品落地页排版：简历、白皮书、作品集、一页纸。羊皮纸暖色 + 靛蓝强调色 + 衬线层级。

---

## 内容创作类

### [long-tail-traffic-strategy](./long-tail-traffic-strategy/) —— 长尾流量策略
挖掘长尾关键词、制定SEO和小红书搜索流量选题、分析用户搜索意图、寻找需求缺口。触发词：长尾词、找词、SEO选题、爆款选题。

### [humanizer](./humanizer/) —— AI痕迹去除
去除AI生成文本的痕迹，使其更自然。基于Wikipedia "Signs of AI writing" 指南。

### [videocut](./videocut/) —— 视频处理套件
包含：高清导出（2-pass编码+锐化）、字幕生成（火山引擎转录）、口播剪辑（口误识别）、自进化（反馈记录）、环境安装。

---

## 生产力工具类

### [book-to-skill](./book-to-skill/) —— 书籍转Skill
将 PDF、EPUB、DOCX、HTML、Markdown 等格式的书籍转换为结构化 Agent Skills，提取框架、心智模型、原则和反模式。

### [huashu-nuwa](./huashu-nuwa/) —— 女娲·Skill造人术
输入人名/主题→自动深度调研→思维框架提炼→生成可运行的人物Skill。触发词：造skill、蒸馏XX、XX的思维方式。

### [find-skills](./find-skills/) —— 技能发现
帮助用户发现和安装 Agent Skills。触发词：怎么实现X、找一个skill、有什么skill可以。

---

## 命理分析类

### [mingli](./mingli/) —— 多维命理分析
整合紫微斗数、八字、印占等多种命理体系，通过交叉验证、逐步推理、质疑检验生成结构化报告。触发词：算命、命理、紫微、八字、流年。

---

## 安装使用

每个 Skill 目录下包含 `SKILL.md` 文件。复制到 `~/.claude/skills/<skill-name>/` 即可使用。

```
~/.claude/skills/
├── mao-zedong-perspective/
│   └── SKILL.md
├── mao-stock-analysis/
│   └── SKILL.md
└── ...
```

---

> 部分 Skill 由 [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill) 生成
> 创建者：[花叔](https://x.com/AlchainHust)
