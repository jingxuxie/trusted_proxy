#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BUNDLE_FILES = [
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_bundle_readme(bundle_dir: Path) -> None:
    lines = [
        "# Trusted by Proxy Submission Bundle",
        "",
        "Anonymous COLM-style workshop submission package.",
        "",
        "## Upload files",
        "",
        "- `main.pdf`: main paper, 5 pages.",
        "- `supplement.pdf`: supplementary material, 2 pages.",
        "",
        "## Verification",
        "",
        "The paper-facing invariant check is:",
        "",
        "```bash",
        "conda run -n trusted_proxy python scripts/check_paper_artifacts.py",
        "```",
        "",
        "The artifact manifest records hashes for the paper, supplement, source,",
        "main task set, saved raw logs, replayed logs, scored runs, and paper tables.",
        "",
        "## Contents",
        "",
    ]
    for src, dst in BUNDLE_FILES:
        source = ROOT / src
        lines.append(f"- `{dst}` from `{src}` ({source.stat().st_size} bytes)")
    (bundle_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_bundle(out_dir: Path, zip_path: Path) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    for src, dst in BUNDLE_FILES:
        source = ROOT / src
        if not source.is_file():
            raise FileNotFoundError(src)
        target = out_dir / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    write_bundle_readme(out_dir)

    if zip_path.exists():
        zip_path.unlink()
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(out_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(out_dir))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="submission/trusted_by_proxy_submission_bundle")
    parser.add_argument("--zip-out", default="submission/trusted_by_proxy_submission_bundle.zip")
    args = parser.parse_args()

    out_dir = ROOT / args.out_dir
    zip_path = ROOT / args.zip_out
    make_bundle(out_dir, zip_path)
    print(f"wrote {out_dir}")
    print(f"wrote {zip_path}")
    print(f"zip sha256 {sha256_file(zip_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
