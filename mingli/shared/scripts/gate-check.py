#!/usr/bin/env python3
"""
紫微斗数 Gate Check — 程序化卡片结构校验

用法:
  python3 gate-check.py <phase_number> <card_file>

示例:
  python3 gate-check.py 0 /tmp/ziwei-phase0-card.md
  python3 gate-check.py 2 ~/Desktop/命理分析-庚辰冬月初七申时男命/phase2-card.md

每个 Phase 有独立的校验规则，只检查结构完整性，不判断内容对错。
退出码: 0=全部通过, 1=有失败项
"""

import sys
import re
import os


# ── 工具函数 ──────────────────────────────────────────────

def count_table_rows(text: str, header_keyword: str) -> int:
    """统计 markdown 表格的数据行数（跳过表头和分隔行）
    从包含 header_keyword 的行开始往下找表格
    """
    lines = text.split("\n")
    in_table = False
    header_found = False
    separator_skipped = False
    row_count = 0

    for line in lines:
        stripped = line.strip()
        # 找到包含关键词的区域
        if not header_found and header_keyword in stripped:
            header_found = True
            continue

        if header_found and not in_table:
            # 找到表头行（含 |）
            if "|" in stripped and stripped.startswith("|"):
                in_table = True
                continue

        if in_table and not separator_skipped:
            # 跳过分隔行 |---|---|
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                separator_skipped = True
                continue

        if in_table and separator_skipped:
            if "|" in stripped and stripped.startswith("|"):
                row_count += 1
            else:
                # 表格结束
                break

    return row_count


def find_table_after(text: str, anchor: str) -> int:
    """在 anchor 关键词之后查找最近的表格，返回数据行数"""
    lines = text.split("\n")
    anchor_idx = -1

    for i, line in enumerate(lines):
        if anchor in line:
            anchor_idx = i
            break

    if anchor_idx == -1:
        return 0

    # 从 anchor 位置向下搜索表格
    in_table = False
    separator_found = False
    row_count = 0

    for line in lines[anchor_idx + 1:]:
        stripped = line.strip()
        if not in_table:
            if "|" in stripped and stripped.startswith("|"):
                in_table = True
                continue
        elif not separator_found:
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                separator_found = True
                continue
            else:
                in_table = False
                separator_found = False
        else:
            if "|" in stripped and stripped.startswith("|"):
                row_count += 1
            else:
                break

    return row_count


def section_exists(text: str, keyword: str) -> bool:
    """检查文本中是否存在包含关键词的段落标题或明确段落"""
    # 检查 markdown 标题
    if re.search(rf"^#+\s*.*{re.escape(keyword)}", text, re.MULTILINE):
        return True
    # 检查加粗标题
    if re.search(rf"\*\*.*{re.escape(keyword)}.*\*\*", text):
        return True
    return False


def keyword_in_text(text: str, keyword: str) -> bool:
    """检查关键词是否出现在文本中"""
    return keyword in text


def count_heading_matches(text: str, pattern: str) -> int:
    """统计匹配特定模式的 ### 标题数量"""
    return len(re.findall(pattern, text, re.MULTILINE))


def count_pattern(text: str, pattern: str) -> int:
    """统计正则模式匹配次数"""
    return len(re.findall(pattern, text))


def has_checkbox_format(text: str, section_keyword: str) -> bool:
    """检查某段落是否包含 checkbox 格式 (- [ ] 或 - [x])"""
    lines = text.split("\n")
    in_section = False
    for line in lines:
        if section_keyword in line:
            in_section = True
            continue
        if in_section:
            if re.match(r"^\s*-\s*\[[ xX]\]", line):
                return True
            # 遇到下一个标题，离开段落
            if re.match(r"^#+\s", line) and section_keyword not in line:
                break
    return False


# ── Phase 校验规则 ────────────────────────────────────────

def check_phase0(text: str) -> list[tuple[bool, str]]:
    """Phase 0: 排盘预检"""
    results = []

    # 基本信息段
    results.append((keyword_in_text(text, "性别"), "基本信息包含'性别'"))
    results.append((keyword_in_text(text, "农历"), "基本信息包含'农历'"))
    results.append((keyword_in_text(text, "真太阳时"), "基本信息包含'真太阳时'"))
    results.append((keyword_in_text(text, "命宫"), "基本信息包含'命宫'"))
    results.append((keyword_in_text(text, "身宫"), "基本信息包含'身宫'"))
    results.append((keyword_in_text(text, "五行局"), "基本信息包含'五行局'"))

    # 十二宫总览表格
    row_count = find_table_after(text, "十二宫")
    if row_count == 0:
        # 尝试其他锚点
        row_count = find_table_after(text, "总览")
    results.append((row_count == 12, f"十二宫总览表格行数 = {row_count} (expected 12)"))

    # 十二宫表格每行包含主星内容（至少非空行）
    if row_count == 12:
        lines = text.split("\n")
        table_start = False
        sep_skipped = False
        non_empty_rows = 0
        for line in lines:
            stripped = line.strip()
            if "十二宫" in stripped or "总览" in stripped:
                table_start = True
                continue
            if table_start and not sep_skipped:
                if "|" in stripped and stripped.startswith("|"):
                    if re.match(r"^\|[\s\-:|]+\|$", stripped):
                        sep_skipped = True
                    continue
            if table_start and sep_skipped:
                if "|" in stripped and stripped.startswith("|"):
                    # 检查表格行中除分隔符外是否有实质内容
                    cells = [c.strip() for c in stripped.split("|")[1:-1]]
                    if any(len(c) > 0 for c in cells):
                        non_empty_rows += 1
                else:
                    break
        results.append((non_empty_rows >= 12,
                         f"十二宫表格非空行数 = {non_empty_rows} (expected >= 12)"))

    # 生年四化
    has_lu = keyword_in_text(text, "化禄")
    has_quan = keyword_in_text(text, "化权")
    has_ke = keyword_in_text(text, "化科")
    has_ji = keyword_in_text(text, "化忌")
    results.append((has_lu, "生年四化包含'化禄'"))
    results.append((has_quan and has_ke and has_ji, "生年四化包含化权/化科/化忌"))

    # 数据来源
    results.append((keyword_in_text(text, "数据来源") or keyword_in_text(text, "来源"),
                     "数据来源标注存在"))

    return results


def check_phase1(text: str) -> list[tuple[bool, str]]:
    """Phase 1: 命盘总论"""
    results = []

    results.append((section_exists(text, "格局") or keyword_in_text(text, "格局定性"),
                     "格局定性段存在"))

    results.append((
        (section_exists(text, "特殊格局") or keyword_in_text(text, "特殊格局")) and
        (has_checkbox_format(text, "特殊格局") or keyword_in_text(text, "[ ]") or keyword_in_text(text, "[x]")),
        "特殊格局段存在且有 checkbox 格式"
    ))

    # 生年四化分析表格
    row_count = find_table_after(text, "四化")
    if row_count == 0:
        row_count = find_table_after(text, "生年四化")
    results.append((row_count == 4, f"生年四化分析表格行数 = {row_count} (expected 4)"))

    results.append((section_exists(text, "来因宫") or keyword_in_text(text, "来因宫"),
                     "来因宫段存在"))

    # 身宫段存在
    results.append((section_exists(text, "身宫") or keyword_in_text(text, "身宫"),
                     "身宫段存在"))

    # 五行局段存在
    results.append((keyword_in_text(text, "五行局") or keyword_in_text(text, "行局"),
                     "五行局段存在"))

    # 四化格局段存在
    has_sihua_pattern = (keyword_in_text(text, "四化格局") or
                         keyword_in_text(text, "双禄") or
                         keyword_in_text(text, "禄忌"))
    results.append((has_sihua_pattern, "四化格局段存在（四化格局/双禄/禄忌）"))

    return results


def check_phase2(text: str) -> list[tuple[bool, str]]:
    """Phase 2: 飞星四化全景"""
    results = []

    # 飞化路径表
    row_count = find_table_after(text, "飞化路径")
    if row_count == 0:
        row_count = find_table_after(text, "路径表")
    results.append((row_count == 12, f"飞化路径表行数 = {row_count} (expected 12)"))

    # 飞化溯源记录
    trace_rows = find_table_after(text, "溯源")
    results.append((trace_rows > 0, f"飞化溯源记录表格行数 = {trace_rows} (expected > 0)"))

    # 飞化路径分类 — 四类标题
    results.append((keyword_in_text(text, "化入我宫") or keyword_in_text(text, "化入"),
                     "飞化路径分类包含'化入我宫'"))
    results.append((keyword_in_text(text, "化出外宫") or keyword_in_text(text, "化出"),
                     "飞化路径分类包含'化出外宫'"))
    results.append((keyword_in_text(text, "化忌冲击") or keyword_in_text(text, "冲击线"),
                     "飞化路径分类包含'化忌冲击线'"))
    results.append((keyword_in_text(text, "自化泄气") or keyword_in_text(text, "自化"),
                     "飞化路径分类包含'自化泄气'"))

    # 飞化闭环
    results.append((section_exists(text, "闭环") or keyword_in_text(text, "飞化闭环"),
                     "飞化闭环段存在"))

    # 忌转忌/忌链
    results.append((keyword_in_text(text, "忌转忌") or keyword_in_text(text, "忌链"),
                     "忌转忌/忌链关键词存在"))

    # 循环忌/互忌
    results.append((keyword_in_text(text, "循环忌") or keyword_in_text(text, "互忌"),
                     "循环忌/互忌关键词存在"))

    # Phase 1 待深入问题回应
    results.append((keyword_in_text(text, "Phase 1") or keyword_in_text(text, "待深入"),
                     "Phase 1待深入问题回应存在"))

    return results


def check_phase3(text: str) -> list[tuple[bool, str]]:
    """Phase 3: 十二宫逐宫"""
    # 宫位名称：支持标准名和别称
    palaces = [
        ("命宫", r"命宫"),
        ("兄弟宫", r"兄弟宫"),
        ("夫妻宫", r"夫妻宫"),
        ("子女宫", r"子女宫"),
        ("财帛宫", r"财帛宫"),
        ("疾厄宫", r"疾厄宫"),
        ("迁移宫", r"迁移宫"),
        ("交友宫", r"交友|仆役|奴仆"),
        ("事业宫", r"官禄|事业宫"),
        ("田宅宫", r"田宅宫"),
        ("福德宫", r"福德宫"),
        ("父母宫", r"父母宫"),
    ]
    results = []

    for display_name, pattern in palaces:
        # 检查是否有该宫的标题（### 或 ## 或 **宫名**）
        has_heading = bool(re.search(
            rf"^#+\s*.*(?:{pattern})", text, re.MULTILINE
        ))
        has_bold = bool(re.search(rf"\*\*(?:{pattern}).*\*\*", text))
        results.append((has_heading or has_bold, f"包含'{display_name}'的分析标题"))

    return results


def check_phase4(text: str) -> list[tuple[bool, str]]:
    """Phase 4: 主题专项"""
    results = []

    # 统计专项分析数量（### 标题中带"专项"或独立的分析主题）
    # 常见专项：事业、财运、感情/婚姻、健康、学业等
    topic_keywords = ["事业", "财运", "感情", "婚姻", "健康", "学业", "人际", "家庭", "投资"]
    topic_count = 0
    for kw in topic_keywords:
        if section_exists(text, kw):
            topic_count += 1

    # 也统计 ### 专项 的数量
    heading_count = count_heading_matches(text, r"^###\s+")
    effective_count = max(topic_count, heading_count)

    results.append((effective_count >= 4,
                     f"专项分析数量 = {effective_count} (expected >= 4)"))

    # 每个专项包含"太极宫位"和"飞化佐证"
    has_taiji = keyword_in_text(text, "太极") or keyword_in_text(text, "立极") or keyword_in_text(text, "核心宫位")
    has_feihua = keyword_in_text(text, "飞化佐证") or keyword_in_text(text, "飞化") and keyword_in_text(text, "佐证")
    results.append((has_taiji, "专项包含'太极宫位/立极'关键词"))
    results.append((has_feihua, "专项包含'飞化佐证'关键词"))

    return results


def check_phase5(text: str) -> list[tuple[bool, str]]:
    """Phase 5: 大限流年"""
    results = []

    # 统计"第N大限"出现次数
    daxian_count = count_pattern(text, r"第[一二三四五六七八九十\d]+大限")
    # 也计算 "大限" 标题出现次数
    if daxian_count == 0:
        daxian_count = count_heading_matches(text, r"^###.*大限")
    results.append((daxian_count >= 6,
                     f"大限分析数量 = {daxian_count} (expected >= 6)"))

    # 关键流年表格
    flow_year_rows = find_table_after(text, "关键流年")
    if flow_year_rows == 0:
        flow_year_rows = find_table_after(text, "流年")
    results.append((flow_year_rows >= 5,
                     f"关键流年表格行数 = {flow_year_rows} (expected >= 5)"))

    # 抽样检查前2个大限段落中包含"宫位"、"主星"、"四化"
    daxian_sections = re.findall(
        r"(第[一二1-2]大限.*?)(?=第[二三四五六七八九十\d]+大限|\Z)",
        text, re.DOTALL
    )
    checked = 0
    for section in daxian_sections[:2]:
        has_gw = keyword_in_text(section, "宫位") or keyword_in_text(section, "宫")
        has_zx = keyword_in_text(section, "主星")
        has_sh = keyword_in_text(section, "四化")
        results.append((has_gw and has_zx and has_sh,
                         f"第{checked+1}大限段落包含宫位+主星+四化"))
        checked += 1
    if checked == 0:
        results.append((False, "未找到大限段落用于抽样检查"))

    # 太岁/流年命宫方法标注
    results.append((keyword_in_text(text, "太岁") or keyword_in_text(text, "流年命宫"),
                     "太岁/流年命宫方法标注存在"))

    return results


def check_phase6(text: str) -> list[tuple[bool, str]]:
    """Phase 6: 综合评判"""
    results = []

    # 关键事件时间线表格
    timeline_rows = find_table_after(text, "时间线")
    if timeline_rows == 0:
        timeline_rows = find_table_after(text, "关键事件")
    results.append((timeline_rows >= 8,
                     f"关键事件时间线表格行数 = {timeline_rows} (expected >= 8)"))

    # 核心优势段
    results.append((section_exists(text, "核心优势") or keyword_in_text(text, "核心优势"),
                     "核心优势段存在"))

    # 确定性标注（双通道匹配，取较大值）
    # 通道1: emoji标记
    emoji_count = count_pattern(text, r"(\u2705|\u26a0\ufe0f|\u274c)")
    # 通道2: 中文关键词
    keyword_count = count_pattern(text, r"(确定性|高确定|中确定|低确定|较确定|确信度|可信度)")
    keyword_count += count_pattern(text, r"[高中低](?:度)?(?:确定|可信)")
    certainty_count = max(emoji_count, keyword_count)
    results.append((certainty_count >= 5,
                     f"确定性标注出现次数 = {certainty_count}（emoji={emoji_count}, 关键词={keyword_count}）(expected >= 5)"))

    # 核心短板
    results.append((keyword_in_text(text, "短板") or keyword_in_text(text, "不足"),
                     "核心短板段存在（短板/不足）"))

    # 策略表行数
    strategy_rows = find_table_after(text, "策略")
    if strategy_rows == 0:
        strategy_rows = find_table_after(text, "阶段策略")
    results.append((strategy_rows >= 4,
                     f"策略表行数 = {strategy_rows} (expected >= 4)"))

    # 极端断语扫描
    extreme_words = re.findall(r"(必定|一定会|绝对|注定)", text)
    results.append((len(extreme_words) == 0,
                     f"极端断语扫描: 发现 {len(extreme_words)} 处（{', '.join(extreme_words[:5])}）" if extreme_words
                     else "极端断语扫描: 无极端断语"))

    # 骑墙检查："一方面"出现次数 > 2 则警告
    fence_count = count_pattern(text, r"一方面")
    results.append((fence_count <= 2,
                     f"骑墙检查: '一方面'出现 {fence_count} 次 (expected <= 2)"))

    return results


# ── 主入口 ────────────────────────────────────────────────

PHASE_CHECKERS = {
    0: check_phase0,
    1: check_phase1,
    2: check_phase2,
    3: check_phase3,
    4: check_phase4,
    5: check_phase5,
    6: check_phase6,
}

PHASE_NAMES = {
    0: "排盘预检",
    1: "命盘总论",
    2: "飞星四化全景",
    3: "十二宫逐宫",
    4: "主题专项",
    5: "大限流年",
    6: "综合评判",
}


def main():
    if len(sys.argv) < 3:
        print("用法: python3 gate-check.py <phase_number> <card_file>")
        print("示例: python3 gate-check.py 0 /tmp/ziwei-phase0-card.md")
        sys.exit(1)

    try:
        phase = int(sys.argv[1])
    except ValueError:
        print(f"错误: phase_number 必须是整数，收到 '{sys.argv[1]}'")
        sys.exit(1)

    if phase not in PHASE_CHECKERS:
        print(f"错误: phase_number 必须在 0-6 之间，收到 {phase}")
        sys.exit(1)

    card_file = sys.argv[2]
    if not os.path.isfile(card_file):
        print(f"错误: 文件不存在 — {card_file}")
        sys.exit(1)

    with open(card_file, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        print(f"错误: 文件为空 — {card_file}")
        sys.exit(1)

    checker = PHASE_CHECKERS[phase]
    results = checker(text)

    # 统计并输出
    passed = sum(1 for ok, _ in results if ok)
    total = len(results)
    all_passed = passed == total

    phase_name = PHASE_NAMES[phase]
    status = "PASS" if all_passed else "FAIL"
    print(f"[{status}] Phase {phase} ({phase_name}) Gate Check: {passed}/{total} assertions passed")

    if not all_passed:
        for ok, desc in results:
            if not ok:
                print(f"  FAIL: {desc}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
