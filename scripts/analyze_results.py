#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import json_pretty, load_jsonl, write_jsonl
from src.scoring import (
    aggregate_by_payload,
    aggregate_scores,
    bootstrap_diff_by_task,
    score_run,
)


def fmt_pct(x: float) -> str:
    return f"{100 * x:.1f}"


def fmt_ci(ci: tuple[float, float]) -> str:
    return f"[{fmt_pct(ci[0])}, {fmt_pct(ci[1])}]"


def write_main_table(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(
            "| Condition | Runs | BSR % | BSR 95% CI | IUSR % | IUSR 95% CI | "
            "ASR % | ASR 95% CI | ATR pp | PDR % | CNAS | Blocks |\n"
        )
        f.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            f.write(
                "| {condition} | {runs} | {bsr} | {bsr_ci} | {iusr} | {iusr_ci} | "
                "{asr} | {asr_ci} | {atr} | {pdr} | {cnas:.2f} | {blocked} |\n".format(
                    condition=row["condition"],
                    runs=row["runs"],
                    bsr=fmt_pct(row["bsr"]),
                    bsr_ci=fmt_ci(row["bsr_ci"]),
                    iusr=fmt_pct(row["iusr"]),
                    iusr_ci=fmt_ci(row["iusr_ci"]),
                    asr=fmt_pct(row["asr"]),
                    asr_ci=fmt_ci(row["asr_ci"]),
                    atr=f"{100 * row['atr']:.1f}",
                    pdr=fmt_pct(row["pdr"]),
                    cnas=row["cnas"],
                    blocked=row["blocked"],
                )
            )


def write_payload_table(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("| Payload class | Condition | Injected runs | ASR % | PDR % |\n")
        f.write("|---|---|---:|---:|---:|\n")
        for row in rows:
            f.write(
                f"| {row['payload_class']} | {row['condition']} | {row['n']} | "
                f"{fmt_pct(row['asr'])} | {fmt_pct(row['pdr'])} |\n"
            )


def write_attack_reason_table(path: Path, scores: list[dict]) -> None:
    injected_by_condition: dict[str, int] = {}
    reason_counts: dict[tuple[str, str], int] = {}
    for score in scores:
        if score["variant"] != "injected":
            continue
        condition = score["condition"]
        injected_by_condition[condition] = injected_by_condition.get(condition, 0) + 1
        for reason in score["attack_reasons"]:
            key = (condition, reason)
            reason_counts[key] = reason_counts.get(key, 0) + 1

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("| Condition | Attack reason | Count | Injected runs | Rate % |\n")
        f.write("|---|---|---:|---:|---:|\n")
        for (condition, reason), count in sorted(reason_counts.items()):
            n = injected_by_condition[condition]
            f.write(f"| {condition} | {reason} | {count} | {n} | {fmt_pct(count / n)} |\n")


def write_trace_examples(path: Path, runs: list[dict], scores: list[dict], max_examples: int = 5) -> None:
    score_by_id = {score["run_id"]: score for score in scores}
    preferred_conditions = [
        "c2x_3agent_extractive_naive",
        "c5x_tracegate_extractive_naive",
        "c3_source_preserving",
        "c4_capability_scoped",
        "c2_3agent_naive",
        "c5_tracegate",
        "c0_single_direct",
    ]

    examples = []
    seen_conditions = set()
    for condition in preferred_conditions:
        for run in runs:
            score = score_by_id[run["run_id"]]
            if run["condition"] != condition or run["task"]["variant"] != "injected":
                continue
            if not (score["attack_success"] or score["blocked_count"] or condition.startswith("c3")):
                continue
            examples.append(
                {
                    "run_id": run["run_id"],
                    "condition": run["condition"],
                    "task_id": run["task"]["task_id"],
                    "payload_class": run["task"]["payload_class"],
                    "attack_success": score["attack_success"],
                    "attack_reasons": score["attack_reasons"],
                    "blocked_count": score["blocked_count"],
                    "reader_output": next(
                        (m["output"] for m in run["agent_messages"] if m["stage"] == "reader"), None
                    ),
                    "planner_output": next(
                        (m["output"] for m in run["agent_messages"] if m["stage"] == "planner"), None
                    ),
                    "tool_log": run["tool_log"],
                }
            )
            seen_conditions.add(condition)
            break
        if len(examples) >= max_examples:
            break

    if len(examples) < max_examples:
        for run in runs:
            if run["condition"] in seen_conditions:
                continue
            score = score_by_id[run["run_id"]]
            if run["task"]["variant"] == "injected" and (score["attack_success"] or score["blocked_count"]):
                examples.append(
                    {
                        "run_id": run["run_id"],
                        "condition": run["condition"],
                        "task_id": run["task"]["task_id"],
                        "payload_class": run["task"]["payload_class"],
                        "attack_success": score["attack_success"],
                        "attack_reasons": score["attack_reasons"],
                        "blocked_count": score["blocked_count"],
                        "reader_output": next(
                            (m["output"] for m in run["agent_messages"] if m["stage"] == "reader"), None
                        ),
                        "planner_output": next(
                            (m["output"] for m in run["agent_messages"] if m["stage"] == "planner"), None
                        ),
                        "tool_log": run["tool_log"],
                    }
                )
            if len(examples) >= max_examples:
                break
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for idx, example in enumerate(examples, start=1):
            f.write(f"## Trace {idx}: {example['condition']} / {example['task_id']}\n\n")
            f.write("```json\n")
            f.write(json_pretty(example))
            f.write("\n```\n\n")


def write_bootstrap_notes(path: Path, scores: list[dict]) -> None:
    present = {
        score["condition"]
        for score in scores
        if score["variant"] == "injected"
    }
    pairs = [
        ("c0_single_direct", "c1_2agent_naive"),
        ("c0_single_direct", "c2_3agent_naive"),
        ("c0_single_direct", "c2x_3agent_extractive_naive"),
        ("c2x_3agent_extractive_naive", "c5x_tracegate_extractive_naive"),
        ("c2x_3agent_extractive_naive", "c6_llm_guard_extractive_naive"),
        ("c2x_3agent_extractive_naive", "c3_source_preserving"),
        ("c2x_3agent_extractive_naive", "c4_capability_scoped"),
        ("c5x_tracegate_extractive_naive", "c6_llm_guard_extractive_naive"),
        ("c0_single_direct", "c2o_3agent_oracle_laundered"),
        ("c2o_3agent_oracle_laundered", "c5o_tracegate_oracle_laundered"),
        ("c2_3agent_naive", "c3_source_preserving"),
        ("c2_3agent_naive", "c4_capability_scoped"),
        ("c2_3agent_naive", "c5_tracegate"),
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("| Comparison | Mean ASR diff pp | Bootstrap 95% CI pp |\n")
        f.write("|---|---:|---:|\n")
        for a, b in pairs:
            if a not in present or b not in present:
                continue
            obs, lo, hi = bootstrap_diff_by_task(scores, a, b)
            f.write(f"| {b} - {a} | {100 * obs:.1f} | [{100 * lo:.1f}, {100 * hi:.1f}] |\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_logs", nargs="+")
    parser.add_argument("--out-dir", default="outputs/scored_runs")
    parser.add_argument("--tables-dir", default="paper/tables")
    args = parser.parse_args()

    runs = []
    for path in args.raw_logs:
        runs.extend(load_jsonl(path))
    scores = [score_run(run) for run in runs]

    out_dir = Path(args.out_dir)
    tables_dir = Path(args.tables_dir)
    write_jsonl(out_dir / "scored_runs.jsonl", scores)
    main_rows = aggregate_scores(scores)
    payload_rows = aggregate_by_payload(scores)
    write_jsonl(out_dir / "main_results.jsonl", main_rows)
    write_jsonl(out_dir / "payload_results.jsonl", payload_rows)
    write_main_table(tables_dir / "main_results.md", main_rows)
    write_payload_table(tables_dir / "payload_results.md", payload_rows)
    write_attack_reason_table(tables_dir / "attack_reason_results.md", scores)
    write_trace_examples(tables_dir / "trace_examples.md", runs, scores)
    write_bootstrap_notes(tables_dir / "bootstrap_notes.md", scores)

    print(f"scored {len(scores)} runs")
    print(f"wrote {tables_dir / 'main_results.md'}")
    print(f"wrote {tables_dir / 'payload_results.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
