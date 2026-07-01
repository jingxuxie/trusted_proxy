#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import load_jsonl, write_jsonl


def group_pairs(tasks: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    grouped: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for task in tasks:
        grouped[task["base_task_id"]][task["variant"]] = task
    missing = {
        base_task_id: sorted({"benign", "injected"} - set(variants))
        for base_task_id, variants in grouped.items()
        if set(variants) != {"benign", "injected"}
    }
    if missing:
        details = ", ".join(f"{base}:{variants}" for base, variants in sorted(missing.items()))
        raise ValueError(f"input does not contain complete benign/injected pairs: {details}")
    return dict(grouped)


def select_pairs(tasks: list[dict[str, Any]], pairs: int) -> list[dict[str, Any]]:
    grouped = group_pairs(tasks)
    selected_base_ids: list[str] = []
    seen_payloads: set[str] = set()

    # Prefer payload coverage first; this makes tiny pilots more informative.
    for task in tasks:
        if task["variant"] != "injected":
            continue
        payload = task["payload_class"]
        base_task_id = task["base_task_id"]
        if payload in seen_payloads or base_task_id in selected_base_ids:
            continue
        selected_base_ids.append(base_task_id)
        seen_payloads.add(payload)
        if len(selected_base_ids) >= pairs:
            break

    # Then preserve source order for larger subsets.
    for task in tasks:
        if len(selected_base_ids) >= pairs:
            break
        base_task_id = task["base_task_id"]
        if base_task_id in selected_base_ids:
            continue
        selected_base_ids.append(base_task_id)

    if len(selected_base_ids) < pairs:
        raise ValueError(f"requested {pairs} pairs but only found {len(selected_base_ids)} complete pairs")

    selected = []
    for base_task_id in selected_base_ids:
        pair = grouped[base_task_id]
        selected.append(pair["benign"])
        selected.append(pair["injected"])
    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--pairs", required=True, type=int)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    if args.pairs <= 0:
        parser.error("--pairs must be positive")

    tasks = load_jsonl(args.input)
    selected = select_pairs(tasks, args.pairs)
    write_jsonl(args.out, selected)

    payloads = [task["payload_class"] for task in selected if task["variant"] == "injected"]
    domains = [task["domain"] for task in selected if task["variant"] == "injected"]
    print(f"wrote {len(selected)} records / {args.pairs} pairs to {args.out}")
    print(f"injected payloads: {payloads}")
    print(f"injected domains: {domains}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
