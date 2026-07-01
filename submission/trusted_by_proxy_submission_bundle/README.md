# Trusted by Proxy Submission Bundle

Anonymous COLM-style workshop submission package.

## Upload files

- `main.pdf`: main paper, 7 pages total; body/ethics fit within pages 1-6.
- `supplement.pdf`: supplementary material, 2 pages.

## Verification

This bundle is an upload package, not a standalone reproduction archive.
Run verification from the full repository root, where the saved logs and
Python scripts are available. The paper-facing invariant check is:

```bash
conda run -n trusted_proxy python scripts/check_paper_artifacts.py
```

The artifact manifest records hashes for the paper, supplement, source,
main task set, saved raw logs, replayed logs, scored runs, and paper tables.
See `REPRODUCE_MAIN_RESULTS.md` in the repository root for the no-API
replay/scoring route.

## Contents

- `main.pdf` from `paper/main.pdf` (132429 bytes)
- `supplement.pdf` from `paper/supplement.pdf` (74670 bytes)
- `ARTIFACT_MANIFEST.md` from `paper/ARTIFACT_MANIFEST.md` (17578 bytes)
- `ARTIFACT_MANIFEST.json` from `paper/ARTIFACT_MANIFEST.json` (24554 bytes)
- `CLAIM_CHECKLIST.md` from `paper/CLAIM_CHECKLIST.md` (6995 bytes)
- `RESULTS_SUMMARY.md` from `paper/RESULTS_SUMMARY.md` (10722 bytes)
- `SUBMISSION_CHECKLIST.md` from `paper/SUBMISSION_CHECKLIST.md` (6813 bytes)
- `COMPLETION_AUDIT.md` from `paper/COMPLETION_AUDIT.md` (11233 bytes)
- `REPRODUCE_MAIN_RESULTS.md` from `REPRODUCE_MAIN_RESULTS.md` (3498 bytes)
- `latex/main.tex` from `paper/main.tex` (23032 bytes)
- `latex/supplement.tex` from `paper/supplement.tex` (5124 bytes)
- `latex/Makefile` from `paper/Makefile` (353 bytes)
- `latex/refs.bib` from `paper/refs.bib` (4897 bytes)
- `latex/colm2026_conference.sty` from `paper/colm2026_conference.sty` (7727 bytes)
- `latex/colm2026_conference.bst` from `paper/colm2026_conference.bst` (26973 bytes)
- `latex/fancyhdr.sty` from `paper/fancyhdr.sty` (20521 bytes)
- `latex/natbib.sty` from `paper/natbib.sty` (45154 bytes)
- `latex/math_commands.tex` from `paper/math_commands.tex` (12284 bytes)
- `TEMPLATE_PROVENANCE.md` from `paper/TEMPLATE_PROVENANCE.md` (1075 bytes)
