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
    "trusted_by_proxy_research_plan.md",
    "slambench/tasks/subtle_multidomain_50pairs_v2.jsonl",
    "outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl",
    "outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl",
    "outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl",
    "outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl",
    "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/scored_runs.jsonl",
    "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.jsonl",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/payload_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/bootstrap_notes.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/attack_reason_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md",
    "paper/main.tex",
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
    "scripts/make_artifact_manifest.py",
    "scripts/make_submission_bundle.py",
    "src/scoring.py",
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
