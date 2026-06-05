#!/usr/bin/env python3
"""
紫微斗数 Trace 落盘 — 每个 Phase 完成后追加 trace 记录

用法:
  python3 trace-writer.py \
    --name "庚辰冬月初七申时男命" \
    --phase 2 \
    --gate-result "PASS" \
    --reasoning-level "heavy" \
    --key-decisions "飞化闭环发现:命宫-疾厄-福德三角;化忌冲击线:田宅宫" \
    --confidence "high" \
    --issues "" \
    --backtrack ""

追加反馈到最近一条记录:
  python3 trace-writer.py \
    --name "庚辰冬月初七申时男命" \
    --feedback "准确" \
    --feedback-detail "事业方向判断准确，婚姻时间偏差2年"

写入路径: ~/Desktop/命理分析-{name}/trace.jsonl
"""

import argparse
import json
import os
import sys
from datetime import datetime

# Phase 名称映射
PHASE_NAMES = {
    0: "排盘预检",
    1: "命盘总论",
    2: "飞星四化全景",
    3: "十二宫逐宫",
    4: "主题专项",
    5: "大限流年",
    6: "综合评判",
}

HARNESS_VERSION = "2026-03-28"


def get_trace_path(name: str) -> str:
    """获取 trace.jsonl 文件路径，目录不存在自动创建"""
    base_dir = os.path.expanduser(f"~/Desktop/命理分析-{name}")
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "trace.jsonl")


def parse_list_field(value: str) -> list[str]:
    """将逗号/分号分隔的字符串解析为列表，空字符串返回空列表"""
    if not value or not value.strip():
        return []
    # 支持中英文分号和逗号
    items = []
    for item in value.replace("；", ";").replace("，", ",").replace(",", ";").split(";"):
        item = item.strip()
        if item:
            items.append(item)
    return items


def write_trace(args: argparse.Namespace) -> None:
    """写入一条 trace 记录"""
    trace_path = get_trace_path(args.name)
    phase = args.phase
    phase_name = PHASE_NAMES.get(phase, f"未知Phase({phase})")

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "name": args.name,
        "phase": phase,
        "phase_name": phase_name,
        "gate_check": args.gate_result.upper(),
        "reasoning_level": args.reasoning_level,
        "key_decisions": parse_list_field(args.key_decisions),
        "confidence": args.confidence,
        "issues": parse_list_field(args.issues),
        "backtrack": args.backtrack if args.backtrack and args.backtrack.strip() else None,
        "harness_version": HARNESS_VERSION,
    }

    with open(trace_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Trace written: Phase {phase} ({phase_name}) -> {trace_path}")


def write_feedback(args: argparse.Namespace) -> None:
    """将反馈追加到最近一条 trace 记录"""
    trace_path = get_trace_path(args.name)

    if not os.path.isfile(trace_path):
        print(f"错误: trace 文件不存在 — {trace_path}")
        sys.exit(1)

    # 读取所有记录
    with open(trace_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print(f"错误: trace 文件为空 — {trace_path}")
        sys.exit(1)

    # 修改最后一条记录
    last_record = json.loads(lines[-1])
    last_record["feedback"] = args.feedback
    if args.feedback_detail:
        last_record["feedback_detail"] = args.feedback_detail

    lines[-1] = json.dumps(last_record, ensure_ascii=False) + "\n"

    with open(trace_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    phase = last_record.get("phase", "?")
    print(f"Feedback appended to Phase {phase} record: {args.feedback}")


def main():
    parser = argparse.ArgumentParser(description="紫微斗数 Trace 落盘")
    parser.add_argument("--name", required=True, help="命主标识")

    # Trace 写入参数
    parser.add_argument("--phase", type=int, help="Phase 编号 (0-6)")
    parser.add_argument("--gate-result", help="Gate Check 结果 (PASS/FAIL)")
    parser.add_argument("--reasoning-level", help="推理强度 (light/medium/heavy)")
    parser.add_argument("--key-decisions", default="", help="关键决策（分号分隔）")
    parser.add_argument("--confidence", help="置信度 (high/medium/low)")
    parser.add_argument("--issues", default="", help="问题（分号分隔）")
    parser.add_argument("--backtrack", default="", help="回溯目标 Phase 或空")

    # 反馈参数
    parser.add_argument("--feedback", help="命主反馈 (准确/不准确/部分准确)")
    parser.add_argument("--feedback-detail", default="", help="反馈详情")

    args = parser.parse_args()

    # 判断模式：反馈 or 写入
    if args.feedback:
        write_feedback(args)
    elif args.phase is not None:
        # 校验必填字段
        missing = []
        if args.gate_result is None:
            missing.append("--gate-result")
        if args.reasoning_level is None:
            missing.append("--reasoning-level")
        if args.confidence is None:
            missing.append("--confidence")
        if missing:
            print(f"错误: 写入 trace 需要以下参数: {', '.join(missing)}")
            sys.exit(1)
        write_trace(args)
    else:
        print("错误: 必须提供 --phase（写入 trace）或 --feedback（追加反馈）")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
