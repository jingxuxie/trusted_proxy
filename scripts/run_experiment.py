#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.backends import OpenAIBackend, SimulatedBackend
from src.common import append_jsonl, load_jsonl
from src.conditions import CONDITIONS, get_condition
from src.runner import run_task


def build_backend(args: argparse.Namespace):
    if args.backend == "simulated":
        return SimulatedBackend(model=args.model or "sim-vulnerable")
    if args.backend == "openai":
        return OpenAIBackend(
            model=args.model,
            api_key_file=args.api_key_file,
            max_output_tokens=args.max_output_tokens,
            temperature=args.temperature,
            request_sleep=args.request_sleep,
        )
    raise ValueError(f"unknown backend: {args.backend}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True)
    parser.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    parser.add_argument("--backend", choices=["simulated", "openai"], default="simulated")
    parser.add_argument("--model", default=None)
    parser.add_argument("--api-key-file", default=None)
    parser.add_argument("--max-output-tokens", type=int, default=500)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--request-sleep", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--variant", choices=["all", "benign", "injected"], default="all")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--resume", action="store_true", help="append to an existing log and skip completed runs")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    if args.backend == "openai" and not args.model:
        parser.error("--model is required for --backend openai")

    tasks = load_jsonl(args.tasks)
    if args.variant != "all":
        tasks = [task for task in tasks if task["variant"] == args.variant]
    if args.limit is not None:
        tasks = tasks[: args.limit]

    condition = get_condition(args.condition)
    backend = build_backend(args)
    out = Path(args.out)
    completed = set()
    if out.exists() and args.resume:
        for run in load_jsonl(out):
            completed.add(
                (
                    run.get("task", {}).get("task_id"),
                    run.get("repeat"),
                    run.get("condition"),
                    run.get("model"),
                )
            )
    elif out.exists():
        out.unlink()

    total = len(tasks) * args.runs
    done = len(completed)
    for repeat in range(args.runs):
        for task in tasks:
            key = (task["task_id"], repeat, condition.condition_id, getattr(backend, "model", None))
            if key in completed:
                continue
            run = run_task(task=task, condition=condition, backend=backend, repeat=repeat)
            append_jsonl(out, run)
            done += 1
            print(f"[{done}/{total}] {condition.condition_id} {task['task_id']} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
