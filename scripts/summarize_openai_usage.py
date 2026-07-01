#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import load_jsonl


FOLLOWUP_PRICE_PRESETS = {
    # Values from followup_experiments_plan.md. Keep prices configurable because
    # API pricing can change independently of the experiment artifacts.
    "gpt-5.5": (5.00, 30.00),
    "gpt-5.4-nano": (0.20, 1.25),
    "gpt-5.4-mini": (0.80, 5.00),
}


def usage_value(usage: dict[str, Any], *keys: str) -> int:
    for key in keys:
        value = usage.get(key)
        if isinstance(value, int | float):
            return int(value)
    return 0


def summarize(paths: list[str], stage: str | None = None) -> list[dict[str, Any]]:
    rows = []
    for path in paths:
        runs = load_jsonl(path)
        input_tokens = 0
        output_tokens = 0
        total_tokens = 0
        calls = 0
        errored_runs = 0
        models = set()
        conditions = set()
        for run in runs:
            if run.get("errors"):
                errored_runs += 1
            if run.get("model"):
                models.add(run["model"])
            conditions.add(run["condition"])
            for message in run.get("agent_messages", []):
                if stage is not None and message.get("stage") != stage:
                    continue
                usage = message.get("usage") or {}
                if usage.get("simulated") or usage.get("oracle_laundered"):
                    continue
                calls += 1
                input_tokens += usage_value(usage, "input_tokens", "prompt_tokens")
                output_tokens += usage_value(usage, "output_tokens", "completion_tokens")
                total_tokens += usage_value(usage, "total_tokens")
        rows.append(
            {
                "path": path,
                "runs": len(runs),
                "calls": calls,
                "conditions": ",".join(sorted(conditions)),
                "models": ",".join(sorted(models)),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "errored_runs": errored_runs,
            }
        )
    return rows


def cost(row: dict[str, Any], input_price: float, output_price: float, scale: float) -> float:
    return scale * (
        row["input_tokens"] / 1_000_000 * input_price
        + row["output_tokens"] / 1_000_000 * output_price
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("logs", nargs="+")
    parser.add_argument("--price-preset", choices=sorted(FOLLOWUP_PRICE_PRESETS), default=None)
    parser.add_argument("--input-price-per-mtok", type=float, default=None)
    parser.add_argument("--output-price-per-mtok", type=float, default=None)
    parser.add_argument("--scale", type=float, default=1.0, help="multiply cost by this projection factor")
    parser.add_argument("--stage", default=None, help="only count usage from this agent message stage")
    args = parser.parse_args()

    if args.price_preset:
        preset_input, preset_output = FOLLOWUP_PRICE_PRESETS[args.price_preset]
    else:
        preset_input, preset_output = None, None
    input_price = args.input_price_per_mtok if args.input_price_per_mtok is not None else preset_input
    output_price = args.output_price_per_mtok if args.output_price_per_mtok is not None else preset_output
    if input_price is None or output_price is None:
        parser.error("pass --price-preset or both explicit price arguments")

    rows = summarize(args.logs, stage=args.stage)
    total_cost = 0.0
    print(
        "| Log | Runs | Calls | Model | Condition | Input toks | Output toks | Total toks | "
        f"Cost x{args.scale:g} | Errors |"
    )
    print("|---|---:|---:|---|---|---:|---:|---:|---:|---:|")
    for row in rows:
        row_cost = cost(row, input_price, output_price, args.scale)
        total_cost += row_cost
        print(
            f"| {Path(row['path']).name} | {row['runs']} | {row['calls']} | {row['models']} | "
            f"{row['conditions']} | {row['input_tokens']} | {row['output_tokens']} | "
            f"{row['total_tokens']} | ${row_cost:.4f} | {row['errored_runs']} |"
        )
    print(f"\nTotal estimated cost at listed prices x{args.scale:g}: ${total_cost:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
