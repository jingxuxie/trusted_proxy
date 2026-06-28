#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.common import load_jsonl


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
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
    "paper/ARTIFACT_MANIFEST.json",
    "paper/ARTIFACT_MANIFEST.md",
    "paper/RESULTS_SUMMARY.md",
    "paper/CLAIM_CHECKLIST.md",
    "paper/SUBMISSION_CHECKLIST.md",
    "paper/COMPLETION_AUDIT.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/payload_results.md",
    "paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md",
    "scripts/make_submission_bundle.py",
    "submission/trusted_by_proxy_submission_bundle/main.pdf",
    "submission/trusted_by_proxy_submission_bundle/supplement.pdf",
    "submission/trusted_by_proxy_submission_bundle/README.md",
    "submission/trusted_by_proxy_submission_bundle.zip",
    "outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl",
    "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.jsonl",
    "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/scored_runs.jsonl",
    "slambench/tasks/subtle_multidomain_50pairs_v2.jsonl",
]

EXPECTED_MAIN = {
    "c0_single_direct": {
        "runs": 100,
        "benign_n": 50,
        "injected_n": 50,
        "bsr": 0.60,
        "iusr": 0.54,
        "asr": 0.06,
        "atr": 0.00,
        "pdr": 0.00,
        "cnas": 0.10,
        "blocked": 0,
    },
    "c2x_3agent_extractive_naive": {
        "runs": 100,
        "benign_n": 50,
        "injected_n": 50,
        "bsr": 0.70,
        "iusr": 0.50,
        "asr": 0.22,
        "atr": 0.16,
        "pdr": 0.77,
        "cnas": 0.31428571428571433,
        "blocked": 0,
    },
    "c5x_tracegate_extractive_naive": {
        "runs": 100,
        "benign_n": 50,
        "injected_n": 50,
        "bsr": 0.66,
        "iusr": 0.64,
        "asr": 0.00,
        "atr": -0.06,
        "pdr": 0.69,
        "cnas": 0.00,
        "blocked": 11,
    },
}

EXPECTED_TEMPLATE_HASHES = {
    "paper/colm2026_conference.sty": "55962ae80c25a50335825c85d23eb5f1cd9015aa8e77f7af32b483b646c7483e",
    "paper/colm2026_conference.bst": "2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5",
    "paper/fancyhdr.sty": "b56ec4434b9f4607529a4b23dc68ad8d4b94f1f631c8cddaf7da78140d53a5ea",
    "paper/natbib.sty": "88bc70c0e48461934cab5b2accef06b74a8b3ac45ad03ccd3f2a6b7e0d6d530d",
    "paper/math_commands.tex": "90473c4d0542070db244cea73ef962d6cddc5b2a746757e6a40ddf5fdfb90ba9",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def assert_close(actual: float, expected: float, *, label: str, tol: float = 1e-9) -> None:
    if abs(actual - expected) > tol:
        fail(f"{label}: expected {expected}, got {actual}")


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing required artifact: {rel}")


def check_template_conformance() -> None:
    for rel in ["paper/main.tex", "paper/supplement.tex"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "\\usepackage[submission]{colm2026_conference}" not in text:
            fail(f"{rel}: missing COLM submission package")
        if "\\usepackage[margin=" in text or "\\usepackage{geometry}" in text:
            fail(f"{rel}: geometry package would violate COLM margins")
        if "\\linenumbers" not in text:
            fail(f"{rel}: missing line numbers for submission mode")
    main_text = (ROOT / "paper/main.tex").read_text(encoding="utf-8")
    if "\\bibliographystyle{colm2026_conference}" not in main_text:
        fail("paper/main.tex: missing COLM bibliography style")
    if "\\section*{Ethics Statement}" not in main_text:
        fail("paper/main.tex: missing ethics statement")
    if "We define a source-laundering attack" not in main_text:
        fail("paper/main.tex: missing formal source-laundering definition")
    provenance = (ROOT / "paper/TEMPLATE_PROVENANCE.md").read_text(encoding="utf-8")
    if "/home/eston/colm_workshop/Template-2026.zip" not in provenance:
        fail("paper/TEMPLATE_PROVENANCE.md: missing requested template archive path")
    if "24c616f7c37769db12fb2f2064b0f55a710b1503d673ba6a3cc114c54c01335e" not in provenance:
        fail("paper/TEMPLATE_PROVENANCE.md: missing requested template archive hash")
    for rel, expected_hash in EXPECTED_TEMPLATE_HASHES.items():
        actual_hash = sha256_file(ROOT / rel)
        if actual_hash != expected_hash:
            fail(f"{rel}: expected template hash {expected_hash}, got {actual_hash}")


def check_main_results() -> None:
    rows = load_jsonl(
        ROOT / "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.jsonl"
    )
    by_condition = {row["condition"]: row for row in rows}
    if set(by_condition) != set(EXPECTED_MAIN):
        fail(f"unexpected main-result conditions: {sorted(by_condition)}")
    for condition, expected in EXPECTED_MAIN.items():
        row = by_condition[condition]
        for key, expected_value in expected.items():
            label = f"{condition}.{key}"
            actual = row.get(key)
            if isinstance(expected_value, float):
                assert_close(float(actual), expected_value, label=label)
            elif actual != expected_value:
                fail(f"{label}: expected {expected_value}, got {actual}")


def check_task_and_run_counts() -> None:
    tasks = load_jsonl(ROOT / "slambench/tasks/subtle_multidomain_50pairs_v2.jsonl")
    if len(tasks) != 100:
        fail(f"task count: expected 100, got {len(tasks)}")
    variants = {
        variant: sum(1 for task in tasks if task["variant"] == variant)
        for variant in {"benign", "injected"}
    }
    if variants != {"benign": 50, "injected": 50}:
        fail(f"task variant counts: expected 50/50, got {variants}")

    replayed = load_jsonl(
        ROOT / "outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl"
    )
    scored = load_jsonl(
        ROOT / "outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/scored_runs.jsonl"
    )
    if len(replayed) != 300:
        fail(f"replayed run count: expected 300, got {len(replayed)}")
    if len(scored) != 300:
        fail(f"scored run count: expected 300, got {len(scored)}")


def check_tracegate_events() -> None:
    replayed = load_jsonl(
        ROOT / "outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl"
    )
    tracegate_runs = [run for run in replayed if run["condition"] == "c5x_tracegate_extractive_naive"]
    audit_sends = 0
    blocks = 0
    sanitized = 0
    for run in tracegate_runs:
        for event in run["tool_log"]:
            if (
                event.get("tool") == "send_email"
                and "audit-log@example.test" in str(event.get("args", {})).lower()
            ):
                audit_sends += 1
            if event.get("tool") == "blocked_tool_call":
                blocks += 1
                if event.get("args", {}).get("sanitized_args"):
                    sanitized += 1
    if audit_sends != 0:
        fail(f"TraceGate audit sends: expected 0, got {audit_sends}")
    if blocks != 11:
        fail(f"TraceGate blocks: expected 11, got {blocks}")
    if sanitized != 5:
        fail(f"TraceGate sanitized mixed-recipient calls: expected 5, got {sanitized}")


def check_pdf_pages(rel: str, expected_pages: int | None) -> None:
    if expected_pages is None:
        return
    try:
        result = subprocess.run(
            ["pdfinfo", str(ROOT / rel)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        fail(f"pdfinfo failed: {exc}")
    pages = None
    for line in result.stdout.splitlines():
        if line.startswith("Pages:"):
            pages = int(line.split(":", 1)[1].strip())
            break
    if pages != expected_pages:
        fail(f"{rel} page count: expected {expected_pages}, got {pages}")


def check_submission_bundle() -> None:
    bundle_dir = ROOT / "submission/trusted_by_proxy_submission_bundle"
    pairs = [
        ("paper/main.pdf", "main.pdf"),
        ("paper/supplement.pdf", "supplement.pdf"),
        ("paper/ARTIFACT_MANIFEST.md", "ARTIFACT_MANIFEST.md"),
        ("paper/ARTIFACT_MANIFEST.json", "ARTIFACT_MANIFEST.json"),
        ("paper/CLAIM_CHECKLIST.md", "CLAIM_CHECKLIST.md"),
        ("paper/RESULTS_SUMMARY.md", "RESULTS_SUMMARY.md"),
        ("paper/SUBMISSION_CHECKLIST.md", "SUBMISSION_CHECKLIST.md"),
        ("paper/COMPLETION_AUDIT.md", "COMPLETION_AUDIT.md"),
        ("paper/main.tex", "latex/main.tex"),
        ("paper/supplement.tex", "latex/supplement.tex"),
        ("paper/refs.bib", "latex/refs.bib"),
        ("paper/colm2026_conference.sty", "latex/colm2026_conference.sty"),
        ("paper/colm2026_conference.bst", "latex/colm2026_conference.bst"),
        ("paper/fancyhdr.sty", "latex/fancyhdr.sty"),
        ("paper/natbib.sty", "latex/natbib.sty"),
        ("paper/math_commands.tex", "latex/math_commands.tex"),
        ("paper/TEMPLATE_PROVENANCE.md", "TEMPLATE_PROVENANCE.md"),
    ]
    for src, dst in pairs:
        source = ROOT / src
        bundled = bundle_dir / dst
        if not bundled.is_file():
            fail(f"submission bundle missing {dst}")
        if sha256_file(source) != sha256_file(bundled):
            fail(f"submission bundle stale copy: {dst}")
    if "Anonymous COLM-style" not in (bundle_dir / "README.md").read_text(encoding="utf-8"):
        fail("submission bundle README missing anonymous COLM package note")


def check_manifest_hashes() -> None:
    manifest_path = ROOT / "paper/ARTIFACT_MANIFEST.json"
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)
    for entry in manifest.get("files", []):
        rel = entry["path"]
        path = ROOT / rel
        if not path.is_file():
            fail(f"manifest file missing: {rel}")
        actual_size = path.stat().st_size
        expected_size = entry["bytes"]
        if actual_size != expected_size:
            fail(f"manifest bytes mismatch for {rel}: expected {expected_size}, got {actual_size}")
        actual_hash = sha256_file(path)
        expected_hash = entry["sha256"]
        if actual_hash != expected_hash:
            fail(f"manifest sha256 mismatch for {rel}: expected {expected_hash}, got {actual_hash}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-main-pages", type=int, default=5)
    parser.add_argument("--expected-supplement-pages", type=int, default=2)
    args = parser.parse_args()

    checks = [
        check_required_files,
        check_template_conformance,
        check_task_and_run_counts,
        check_main_results,
        check_tracegate_events,
        lambda: check_pdf_pages("paper/main.pdf", args.expected_main_pages),
        lambda: check_pdf_pages("paper/supplement.pdf", args.expected_supplement_pages),
        check_submission_bundle,
        check_manifest_hashes,
    ]
    for check in checks:
        check()
    print("paper artifact check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
