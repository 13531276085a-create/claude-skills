"""断卦 trace 日志 — 每次断卦记录结构化JSON，用于迭代分析"""

import json
import os
from datetime import datetime
from pathlib import Path

TRACES_DIR = Path(__file__).parent / "traces"


def ensure_dir():
    TRACES_DIR.mkdir(exist_ok=True)


def create_trace(input_time, question, paipan_result):
    """创建一条新的断卦 trace。返回 trace_id。"""
    ensure_dir()
    trace_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    trace = {
        "trace_id": trace_id,
        "created_at": datetime.now().isoformat(),
        "input": {
            "time": input_time,
            "question": question,
        },
        "paipan": {
            "四柱": paipan_result.get("四柱"),
            "定局": paipan_result.get("定局"),
            "值符值使": paipan_result.get("值符值使"),
        },
        "verify": {"passed": None, "errors": [], "checks": 0},
        "sop_steps": {},
        "evaluator": {"result": None, "issues": [], "corrections": []},
        "user_feedback": None,
    }
    _write(trace_id, trace)
    return trace_id


def log_verify(trace_id, passed, errors, checks):
    """记录自检结果。"""
    trace = _read(trace_id)
    trace["verify"] = {
        "passed": passed,
        "errors": errors,
        "checks": checks,
    }
    _write(trace_id, trace)


def log_sop_step(trace_id, step_num, step_name, summary, issues=None):
    """记录单步SOP解读摘要。"""
    trace = _read(trace_id)
    trace["sop_steps"][str(step_num)] = {
        "name": step_name,
        "summary": summary,
        "issues": issues or [],
    }
    _write(trace_id, trace)


def log_evaluator(trace_id, result, issues=None, corrections=None):
    """记录 evaluator 复核结果。"""
    trace = _read(trace_id)
    trace["evaluator"] = {
        "result": result,
        "issues": issues or [],
        "corrections": corrections or [],
    }
    _write(trace_id, trace)


def log_feedback(trace_id, feedback):
    """记录用户反馈。"""
    trace = _read(trace_id)
    trace["user_feedback"] = feedback
    _write(trace_id, trace)


def list_traces():
    """列出所有 trace 文件。"""
    ensure_dir()
    files = sorted(TRACES_DIR.glob("*.json"))
    return [f.stem for f in files]


def get_trace(trace_id):
    """读取单条 trace。"""
    return _read(trace_id)


def _read(trace_id):
    path = TRACES_DIR / f"{trace_id}.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write(trace_id, data):
    ensure_dir()
    path = TRACES_DIR / f"{trace_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
