#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.backends import BaseBackend, BackendResult, OpenAIBackend
from src.common import append_jsonl, load_jsonl
from src.conditions import CONDITIONS, get_condition
from src.runner import run_task


class StageBackend(BaseBackend):
    backend_id = "openai_heterogeneous"

    def __init__(self, backends: dict[str, OpenAIBackend]):
        self.backends = backends
        self.model = ",".join(f"{stage}:{backend.model}" for stage, backend in sorted(backends.items()))

    def generate(
        self,
        *,
        stage: str,
        task: dict[str, Any],
        defense: str,
        messages: list[dict[str, str]],
        prior_outputs: dict[str, Any],
    ) -> BackendResult:
        backend = self.backends.get(stage)
        if backend is None:
            backend = self.backends["default"]
        return backend.generate(
            stage=stage,
            task=task,
            defense=defense,
            messages=messages,
            prior_outputs=prior_outputs,
        )


def build_backend(args: argparse.Namespace) -> StageBackend:
    kwargs = {
        "api_key_file": args.api_key_file,
        "max_output_tokens": args.max_output_tokens,
        "temperature": args.temperature,
        "request_sleep": args.request_sleep,
    }
    default = OpenAIBackend(model=args.default_model, **kwargs)
    backends = {"default": default}
    for stage, model in {
        "direct_executor": args.direct_model,
        "reader": args.reader_model,
        "planner": args.planner_model,
        "executor": args.executor_model,
    }.items():
        if model is not None:
            backends[stage] = OpenAIBackend(model=model, **kwargs)
    return StageBackend(backends)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True)
    parser.add_argument("--condition", required=True, choices=sorted(CONDITIONS))
    parser.add_argument("--api-key-file", default=None)
    parser.add_argument("--default-model", required=True)
    parser.add_argument("--direct-model", default=None)
    parser.add_argument("--reader-model", default=None)
    parser.add_argument("--planner-model", default=None)
    parser.add_argument("--executor-model", default=None)
    parser.add_argument("--max-output-tokens", type=int, default=900)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--request-sleep", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--variant", choices=["all", "benign", "injected"], default="all")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

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
            key = (task["task_id"], repeat, condition.condition_id, backend.model)
            if key in completed:
                continue
            run = run_task(task=task, condition=condition, backend=backend, repeat=repeat)
            run["heterogeneous_models"] = {
                "default": args.default_model,
                "direct_executor": args.direct_model,
                "reader": args.reader_model,
                "planner": args.planner_model,
                "executor": args.executor_model,
            }
            append_jsonl(out, run)
            done += 1
            print(f"[{done}/{total}] {condition.condition_id} {task['task_id']} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
