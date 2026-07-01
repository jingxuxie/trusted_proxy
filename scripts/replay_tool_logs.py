#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import load_jsonl, write_jsonl
from src.conditions import get_condition
from src.tool_call_extraction import extract_tool_calls
from src.tools import MockEnv, execute_tool_calls


def replay_run(run: dict, as_condition: str | None = None) -> dict:
    task = run["task"]
    original_condition = run["condition"]
    condition_id = as_condition or original_condition
    condition = get_condition(condition_id)
    env = MockEnv(task)

    for artifact in task["untrusted_artifacts"]:
        env.read_doc(artifact["source_id"])

    for message in run.get("agent_messages", []):
        stage = message.get("stage")
        if stage not in {"direct_executor", "executor"}:
            continue
        tool_calls = extract_tool_calls(message.get("output", {}) or {}, task["allowed_tools"])
        execute_tool_calls(env, tool_calls, tracegate=condition.tracegate)

    replayed = dict(run)
    replayed["condition"] = condition.condition_id
    replayed["topology"] = condition.topology
    replayed["defense"] = condition.defense
    replayed["tool_log"] = env.log
    replayed["replay"] = {
        "source_run_id": run["run_id"],
        "source_condition": original_condition,
        "as_condition": condition.condition_id,
        "note": "Replayed saved agent outputs through current tool-call canonicalization and condition runtime.",
    }
    return replayed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_logs", nargs="+")
    parser.add_argument("--as-condition", default=None, help="replay saved outputs under this condition runtime")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    replayed = []
    for path in args.raw_logs:
        replayed.extend(replay_run(run, as_condition=args.as_condition) for run in load_jsonl(path))

    write_jsonl(args.out, replayed)
    print(f"replayed {len(replayed)} runs to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
