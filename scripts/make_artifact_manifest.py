#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import load_jsonl


ROOT = Path(__file__).resolve().parents[1]

MANIFEST_FILES = [
    "README.md",
    "REPRODUCE_MAIN_RESULTS.md",
    "trusted_by_proxy_research_plan.md",
    "followup_experiments_plan.md",
    "slambench/tasks/dev_30.jsonl",
    "slambench/tasks/subtle_multidomain_50pairs_v2.jsonl",
    "slambench/tasks/subtle_multidomain_25pairs_v2.jsonl",
    "slambench/tasks/subtle_multidomain_5pairs_v2.jsonl",
    "slambench/tasks/subtle_multidomain_repeatability_6inj_v2.jsonl",
    "slambench/tasks/subtle_multidomain_hard6pairs_v2.jsonl",
    "slambench/tasks/nonemail_side_effects_3pairs_v1.jsonl",
    "outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl",
    "outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl",
    "outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl",
    "outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl",
    "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/scored_runs.jsonl",
    "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.jsonl",
    "outputs/raw_logs/followup_gpt55_25pairs_1200_c0.jsonl",
    "outputs/raw_logs/followup_gpt55_25pairs_1200_c2x.jsonl",
    "outputs/raw_logs/followup_gpt55_25pairs_1200_c5x.jsonl",
    "outputs/scored_runs/followup_gpt55_25pairs_1200_core/scored_runs.jsonl",
    "outputs/scored_runs/followup_gpt55_25pairs_1200_core/main_results.jsonl",
    "outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl",
    "outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c1.jsonl",
    "outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2.jsonl",
    "outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl",
    "outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2o.jsonl",
    "outputs/scored_runs/followup_gpt54nano_25pairs_1200_topology/scored_runs.jsonl",
    "outputs/scored_runs/followup_gpt54nano_25pairs_1200_topology/main_results.jsonl",
    "outputs/analysis/followup_gpt54nano_25pairs_1200_topology_mechanism/provenance_flow_runs.jsonl",
    "outputs/analysis/followup_gpt54nano_25pairs_1200_topology_mechanism/provenance_flow_summary.jsonl",
    "outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c3.jsonl",
    "outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c4.jsonl",
    "outputs/replayed_logs/followup_gpt54nano_25pairs_1200_defense_c5x_replay_from_c2x.jsonl",
    "outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense/scored_runs.jsonl",
    "outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense/main_results.jsonl",
    "outputs/analysis/followup_gpt54nano_25pairs_1200_defense_mechanism/provenance_flow_runs.jsonl",
    "outputs/analysis/followup_gpt54nano_25pairs_1200_defense_mechanism/provenance_flow_summary.jsonl",
    "outputs/replayed_logs/followup_gpt54nano_25pairs_1200_guard_c6_from_c2x.jsonl",
    "outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_guard/scored_runs.jsonl",
    "outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_guard/main_results.jsonl",
    "outputs/raw_logs/followup_gpt54nano_repeatability_6inj_c0_3runs.jsonl",
    "outputs/raw_logs/followup_gpt54nano_repeatability_6inj_c2x_3runs.jsonl",
    "outputs/replayed_logs/followup_gpt54nano_repeatability_6inj_c5x_replay_from_c2x_3runs.jsonl",
    "outputs/scored_runs/followup_gpt54nano_repeatability_6inj_3runs/scored_runs.jsonl",
    "outputs/scored_runs/followup_gpt54nano_repeatability_6inj_3runs/main_results.jsonl",
    "outputs/raw_logs/followup_gpt54nano_nonemail_3pairs_c0.jsonl",
    "outputs/raw_logs/followup_gpt54nano_nonemail_3pairs_c2x.jsonl",
    "outputs/replayed_logs/followup_gpt54nano_nonemail_3pairs_c5x_replay_from_c2x.jsonl",
    "outputs/scored_runs/followup_gpt54nano_nonemail_3pairs/scored_runs.jsonl",
    "outputs/scored_runs/followup_gpt54nano_nonemail_3pairs/main_results.jsonl",
    "outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x.jsonl",
    "outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x_with_parser_error.jsonl",
    "outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x_repair_research_subtle_002.jsonl",
    "outputs/scored_runs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/scored_runs.jsonl",
    "outputs/scored_runs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/main_results.jsonl",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/payload_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/bootstrap_notes.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/attack_reason_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md",
    "paper/tables/followup_gpt55_25pairs_1200_core/RESULT_SUMMARY.md",
    "paper/tables/followup_gpt55_25pairs_1200_core/main_results.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_topology/RESULT_SUMMARY.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_topology/main_results.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism/provenance_flow_summary.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism/differential_attack_cases.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_defense/RESULT_SUMMARY.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_defense/main_results.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism/provenance_flow_summary.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism/differential_attack_cases.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/RESULT_SUMMARY.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/main_results.md",
    "paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/bootstrap_notes.md",
    "paper/tables/followup_gpt54nano_repeatability_6inj_3runs/RESULT_SUMMARY.md",
    "paper/tables/followup_gpt54nano_repeatability_6inj_3runs/main_results.md",
    "paper/tables/followup_gpt54nano_nonemail_3pairs/RESULT_SUMMARY.md",
    "paper/tables/followup_gpt54nano_nonemail_3pairs/main_results.md",
    "paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/RESULT_SUMMARY.md",
    "paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/main_results.md",
    "paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/payload_results.md",
    "paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/hard_slice_comparison.md",
    "paper/main.tex",
    "paper/Makefile",
    "paper/main.pdf",
    "paper/supplement.tex",
    "paper/supplement.pdf",
    "paper/colm2026_conference.sty",
    "paper/colm2026_conference.bst",
    "paper/fancyhdr.sty",
    "paper/natbib.sty",
    "paper/math_commands.tex",
    "paper/TEMPLATE_PROVENANCE.md",
    "paper/refs.bib",
    "paper/RESULTS_SUMMARY.md",
    "paper/CLAIM_CHECKLIST.md",
    "paper/SUBMISSION_CHECKLIST.md",
    "paper/COMPLETION_AUDIT.md",
    "scripts/check_paper_artifacts.py",
    "scripts/analyze_results.py",
    "scripts/analyze_provenance_flow.py",
    "scripts/validate_tasks.py",
    "scripts/generate_subtle_multidomain_tasks.py",
    "scripts/generate_nonemail_side_effect_tasks.py",
    "scripts/make_artifact_manifest.py",
    "scripts/make_submission_bundle.py",
    "scripts/make_paired_subset.py",
    "scripts/replay_tool_logs.py",
    "scripts/replay_with_llm_guard.py",
    "scripts/run_heterogeneous_experiment.py",
    "scripts/run_experiment.py",
    "scripts/summarize_openai_usage.py",
    "src/scoring.py",
    "src/tools.py",
    "tests/test_scoring.py",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jsonl_count(path: Path) -> int | None:
    if path.suffix != ".jsonl":
        return None
    return len(load_jsonl(path))


def pdf_pages(path: Path) -> int | None:
    if path.suffix != ".pdf":
        return None
    result = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    return None


def file_entry(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(rel)
    entry: dict[str, Any] = {
        "path": rel,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    records = jsonl_count(path)
    if records is not None:
        entry["records"] = records
    pages = pdf_pages(path)
    if pages is not None:
        entry["pages"] = pages
    return entry


def main_metrics() -> list[dict[str, Any]]:
    rows = load_jsonl(
        ROOT / "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.jsonl"
    )
    keys = ["condition", "runs", "bsr", "iusr", "asr", "atr", "pdr", "cnas", "blocked"]
    return [{key: row[key] for key in keys} for row in rows]


def build_manifest() -> dict[str, Any]:
    return {
        "name": "Trusted by Proxy paper artifact manifest",
        "main_task_set": "slambench/tasks/subtle_multidomain_50pairs_v2.jsonl",
        "main_model": "gpt-5.4-nano",
        "main_conditions": [
            "c0_single_direct",
            "c2x_3agent_extractive_naive",
            "c5x_tracegate_extractive_naive",
        ],
        "main_metrics": main_metrics(),
        "files": [file_entry(rel) for rel in MANIFEST_FILES],
    }


def write_json(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, sort_keys=True, indent=2)
        f.write("\n")


def write_markdown(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Trusted by Proxy Artifact Manifest",
        "",
        "This manifest records the paper-facing artifacts used for the current main claim.",
        "Regenerate it with `conda run -n trusted_proxy python scripts/make_artifact_manifest.py`.",
        "",
        "## Main Metrics",
        "",
        "| Condition | Runs | BSR | IUSR | ASR | ATR | PDR | CNAS | Blocks |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in manifest["main_metrics"]:
        lines.append(
            "| {condition} | {runs} | {bsr:.2f} | {iusr:.2f} | {asr:.2f} | "
            "{atr:.2f} | {pdr:.2f} | {cnas:.2f} | {blocked} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            "| Path | Bytes | Records/Pages | SHA256 |",
            "|---|---:|---:|---|",
        ]
    )
    for entry in manifest["files"]:
        count = entry.get("records", entry.get("pages", ""))
        lines.append(f"| `{entry['path']}` | {entry['bytes']} | {count} | `{entry['sha256']}` |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", default="paper/ARTIFACT_MANIFEST.json")
    parser.add_argument("--md-out", default="paper/ARTIFACT_MANIFEST.md")
    args = parser.parse_args()

    manifest = build_manifest()
    write_json(ROOT / args.json_out, manifest)
    write_markdown(ROOT / args.md_out, manifest)
    print(f"wrote {args.json_out}")
    print(f"wrote {args.md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
