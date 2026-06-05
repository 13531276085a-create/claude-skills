"""断卦 trace 批量分析 — 从 traces/ 读取所有记录，输出失败模式报告"""

import json
import sys
from collections import Counter
from pathlib import Path

TRACES_DIR = Path(__file__).parent / "traces"


def load_all():
    if not TRACES_DIR.exists():
        print("traces/ 目录不存在，尚无断卦记录。")
        return []
    files = sorted(TRACES_DIR.glob("*.json"))
    traces = []
    for f in files:
        with open(f, encoding="utf-8") as fp:
            traces.append(json.load(fp))
    return traces


def analyze(traces):
    total = len(traces)
    if total == 0:
        print("无 trace 数据。")
        return

    # 1. 自检统计
    verify_pass = sum(1 for t in traces if t["verify"]["passed"])
    verify_fail = total - verify_pass
    verify_error_types = Counter()
    for t in traces:
        for err in t["verify"]["errors"]:
            # 提取 [步骤] 标签
            if err.startswith("["):
                tag = err.split("]")[0] + "]"
                verify_error_types[tag] += 1

    # 2. Evaluator 统计
    eval_pass = sum(1 for t in traces if t["evaluator"]["result"] == "通过")
    eval_warn = sum(1 for t in traces if t["evaluator"]["result"] == "有疑点")
    eval_fail = sum(1 for t in traces if t["evaluator"]["result"] == "有矛盾")
    eval_no = sum(1 for t in traces if t["evaluator"]["result"] is None)
    eval_issue_types = Counter()
    for t in traces:
        for issue in t["evaluator"]["issues"]:
            # 提取类型标签 [矛盾]/[遗漏]/[方向错]
            if issue.startswith("["):
                tag = issue.split("]")[0] + "]"
                eval_issue_types[tag] += 1
            else:
                eval_issue_types["[未分类]"] += 1

    # 3. SOP 步骤问题分布
    sop_issues = Counter()
    for t in traces:
        for step_num, step_data in t["sop_steps"].items():
            if step_data.get("issues"):
                sop_issues[f"第{step_num}步·{step_data['name']}"] += len(step_data["issues"])

    # 4. 用户反馈
    feedback_given = sum(1 for t in traces if t["user_feedback"] is not None)

    # 输出报告
    print(f"{'='*60}")
    print(f"断卦 Trace 分析报告 | 共 {total} 条记录")
    print(f"{'='*60}")

    print(f"\n## 1. 排盘自检")
    print(f"通过: {verify_pass} | 失败: {verify_fail}")
    if verify_error_types:
        print(f"失败分布:")
        for tag, cnt in verify_error_types.most_common(10):
            print(f"  {tag}: {cnt}次")

    print(f"\n## 2. Evaluator 复核")
    print(f"通过: {eval_pass} | 有疑点: {eval_warn} | 有矛盾: {eval_fail} | 未执行: {eval_no}")
    if eval_no > 0:
        print(f"  ⚠️ {eval_no} 次断卦跳过了 evaluator 复核!")
    if eval_issue_types:
        print(f"问题分布:")
        for tag, cnt in eval_issue_types.most_common(10):
            print(f"  {tag}: {cnt}次")

    print(f"\n## 3. SOP 步骤问题热点")
    if sop_issues:
        for step, cnt in sop_issues.most_common():
            print(f"  {step}: {cnt}个问题")
    else:
        print("  无记录（SOP步骤未记录问题，或全部无问题）")

    print(f"\n## 4. 用户反馈")
    print(f"已收集: {feedback_given}/{total}")

    # 5. Evaluator 跳过率
    if total > 0:
        skip_rate = eval_no / total * 100
        if skip_rate > 0:
            print(f"\n## ⚠️ 警告")
            print(f"Evaluator 跳过率: {skip_rate:.0f}% — 需要加强强制执行")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    traces = load_all()
    analyze(traces)
