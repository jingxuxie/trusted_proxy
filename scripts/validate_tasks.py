#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import load_jsonl


REQUIRED_KEYS = {
    "task_id",
    "base_task_id",
    "domain",
    "variant",
    "payload_class",
    "user_goal",
    "trusted_context",
    "untrusted_artifacts",
    "allowed_tools",
    "expected_benign_outcome",
    "forbidden_outcome",
    "reference_benign_tool_calls",
    "attack_tool_call",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks")
    args = parser.parse_args()
    tasks = load_jsonl(args.tasks)
    errors = []
    seen = set()
    for idx, task in enumerate(tasks, start=1):
        missing = REQUIRED_KEYS - set(task)
        if missing:
            errors.append(f"record {idx}: missing {sorted(missing)}")
        if task.get("task_id") in seen:
            errors.append(f"record {idx}: duplicate task_id {task.get('task_id')}")
        seen.add(task.get("task_id"))
        if task.get("variant") not in {"benign", "injected"}:
            errors.append(f"record {idx}: bad variant {task.get('variant')}")
        if not task.get("untrusted_artifacts"):
            errors.append(f"record {idx}: no artifact")
        for call in task.get("reference_benign_tool_calls", []):
            if call.get("tool") not in task.get("allowed_tools", []):
                errors.append(f"record {idx}: benign call uses disallowed tool {call.get('tool')}")
        if task.get("attack_tool_call", {}).get("tool") not in task.get("allowed_tools", []):
            errors.append(f"record {idx}: attack call uses disallowed tool")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"validated {len(tasks)} task records from {args.tasks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

