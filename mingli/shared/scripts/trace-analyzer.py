#!/usr/bin/env python3
"""
紫微斗数 Trace 失败模式分析 — 批量分析多份 trace.jsonl

用法:
  python3 trace-analyzer.py ~/Desktop/命理分析-*/trace.jsonl

分析维度:
  1. Phase 失败率
  2. 回溯频率
  3. 低置信度分布
  4. 常见 issues
  5. 命主反馈汇总
"""

import json
import sys
import os
import glob as glob_mod
from collections import Counter, defaultdict

PHASE_NAMES = {
    0: "排盘预检",
    1: "命盘总论",
    2: "飞星四化全景",
    3: "十二宫逐宫",
    4: "主题专项",
    5: "大限流年",
    6: "综合评判",
}


def load_traces(file_patterns: list[str]) -> list[dict]:
    """加载所有 trace 记录，支持 glob 模式"""
    records = []
    files_loaded = set()

    for pattern in file_patterns:
        # 展开 glob
        matched = glob_mod.glob(os.path.expanduser(pattern))
        if not matched:
            print(f"警告: 未匹配到文件 — {pattern}", file=sys.stderr)
            continue

        for filepath in matched:
            if filepath in files_loaded:
                continue
            files_loaded.add(filepath)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            records.append(json.loads(line))
                        except json.JSONDecodeError:
                            print(f"警告: JSON 解析失败 — {filepath}:{line_num}",
                                  file=sys.stderr)
            except OSError as e:
                print(f"警告: 无法读取 — {filepath}: {e}", file=sys.stderr)

    return records


def analyze_phase_failures(records: list[dict]) -> str:
    """分析每个 Phase 的 Gate Check 失败率"""
    phase_stats: dict[int, dict[str, int]] = defaultdict(lambda: {"total": 0, "fail": 0})

    for r in records:
        phase = r.get("phase")
        if phase is None:
            continue
        phase_stats[phase]["total"] += 1
        if r.get("gate_check", "").upper() == "FAIL":
            phase_stats[phase]["fail"] += 1

    if not phase_stats:
        return "无数据\n"

    lines = ["| Phase | 名称 | 总次数 | 失败次数 | 失败率 |",
             "|-------|------|--------|---------|--------|"]

    for phase in sorted(phase_stats.keys()):
        s = phase_stats[phase]
        rate = f"{s['fail'] / s['total'] * 100:.1f}%" if s["total"] > 0 else "N/A"
        name = PHASE_NAMES.get(phase, f"Phase {phase}")
        lines.append(f"| {phase} | {name} | {s['total']} | {s['fail']} | {rate} |")

    return "\n".join(lines) + "\n"


def analyze_backtracks(records: list[dict]) -> str:
    """分析回溯频率"""
    backtrack_counter: Counter = Counter()
    total_records = 0

    for r in records:
        total_records += 1
        bt = r.get("backtrack")
        if bt:
            backtrack_counter[str(bt)] += 1

    if not backtrack_counter:
        return "无回溯记录\n"

    total_backtracks = sum(backtrack_counter.values())
    lines = [f"总记录数: {total_records}, 触发回溯: {total_backtracks} "
             f"({total_backtracks / total_records * 100:.1f}%)\n",
             "| 回溯目标 | 次数 | 占比 |",
             "|----------|------|------|"]

    for target, count in backtrack_counter.most_common():
        pct = f"{count / total_records * 100:.1f}%"
        lines.append(f"| {target} | {count} | {pct} |")

    return "\n".join(lines) + "\n"


def analyze_low_confidence(records: list[dict]) -> str:
    """分析低置信度分布"""
    phase_confidence: dict[int, Counter] = defaultdict(Counter)

    for r in records:
        phase = r.get("phase")
        conf = r.get("confidence", "unknown")
        if phase is not None:
            phase_confidence[phase][conf] += 1

    if not phase_confidence:
        return "无数据\n"

    lines = ["| Phase | 名称 | high | medium | low | low 占比 |",
             "|-------|------|------|--------|-----|---------|"]

    for phase in sorted(phase_confidence.keys()):
        c = phase_confidence[phase]
        total = sum(c.values())
        low = c.get("low", 0)
        rate = f"{low / total * 100:.1f}%" if total > 0 else "N/A"
        name = PHASE_NAMES.get(phase, f"Phase {phase}")
        lines.append(
            f"| {phase} | {name} | {c.get('high', 0)} | {c.get('medium', 0)} | "
            f"{low} | {rate} |"
        )

    return "\n".join(lines) + "\n"


def analyze_common_issues(records: list[dict]) -> str:
    """按频次排序的 issue 类型"""
    issue_counter: Counter = Counter()

    for r in records:
        issues = r.get("issues", [])
        if isinstance(issues, list):
            for issue in issues:
                if issue:
                    issue_counter[issue] += 1
        elif isinstance(issues, str) and issues:
            issue_counter[issues] += 1

    if not issue_counter:
        return "无 issues 记录\n"

    lines = ["| Issue | 出现次数 |",
             "|-------|---------|"]

    for issue, count in issue_counter.most_common(20):
        lines.append(f"| {issue} | {count} |")

    return "\n".join(lines) + "\n"


def analyze_feedback(records: list[dict]) -> str:
    """命主反馈汇总"""
    feedback_counter: Counter = Counter()
    feedback_details: list[tuple[str, str, str]] = []  # (name, feedback, detail)

    for r in records:
        fb = r.get("feedback")
        if fb:
            feedback_counter[fb] += 1
            detail = r.get("feedback_detail", "")
            name = r.get("name", "未知")
            if detail:
                feedback_details.append((name, fb, detail))

    if not feedback_counter:
        return "无反馈记录\n"

    total = sum(feedback_counter.values())
    lines = ["| 反馈类型 | 次数 | 占比 |",
             "|----------|------|------|"]
    for fb, count in feedback_counter.most_common():
        pct = f"{count / total * 100:.1f}%"
        lines.append(f"| {fb} | {count} | {pct} |")

    if feedback_details:
        lines.append("")
        lines.append("**反馈详情:**")
        lines.append("")
        for name, fb, detail in feedback_details:
            lines.append(f"- **{name}** [{fb}]: {detail}")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 trace-analyzer.py ~/Desktop/命理分析-*/trace.jsonl")
        sys.exit(1)

    file_patterns = sys.argv[1:]
    records = load_traces(file_patterns)

    if not records:
        print("错误: 未加载到任何 trace 记录")
        sys.exit(1)

    # 统计基本信息
    unique_names = set(r.get("name", "") for r in records)
    print(f"# 紫微斗数 Trace 分析报告\n")
    print(f"- 案例数: {len(unique_names)}")
    print(f"- 总记录数: {len(records)}")
    print()

    print("## 1. Phase 失败率\n")
    print(analyze_phase_failures(records))

    print("## 2. 回溯频率\n")
    print(analyze_backtracks(records))

    print("## 3. 低置信度分布\n")
    print(analyze_low_confidence(records))

    print("## 4. 常见 Issues\n")
    print(analyze_common_issues(records))

    print("## 5. 命主反馈汇总\n")
    print(analyze_feedback(records))


if __name__ == "__main__":
    main()
