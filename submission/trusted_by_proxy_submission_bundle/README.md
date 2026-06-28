# Trusted by Proxy Submission Bundle

Anonymous COLM-style workshop submission package.

## Upload files

- `main.pdf`: main paper, 5 pages.
- `supplement.pdf`: supplementary material, 2 pages.

## Verification

The paper-facing invariant check is:

```bash
conda run -n trusted_proxy python scripts/check_paper_artifacts.py
```

The artifact manifest records hashes for the paper, supplement, source,
main task set, saved raw logs, replayed logs, scored runs, and paper tables.

## Contents

- `main.pdf` from `paper/main.pdf` (107666 bytes)
- `supplement.pdf` from `paper/supplement.pdf` (74670 bytes)
- `ARTIFACT_MANIFEST.md` from `paper/ARTIFACT_MANIFEST.md` (5082 bytes)
- `ARTIFACT_MANIFEST.json` from `paper/ARTIFACT_MANIFEST.json` (7234 bytes)
- `CLAIM_CHECKLIST.md` from `paper/CLAIM_CHECKLIST.md` (3809 bytes)
- `RESULTS_SUMMARY.md` from `paper/RESULTS_SUMMARY.md` (8929 bytes)
- `SUBMISSION_CHECKLIST.md` from `paper/SUBMISSION_CHECKLIST.md` (5484 bytes)
- `COMPLETION_AUDIT.md` from `paper/COMPLETION_AUDIT.md` (4853 bytes)
- `latex/main.tex` from `paper/main.tex` (15706 bytes)
- `latex/supplement.tex` from `paper/supplement.tex` (5124 bytes)
- `latex/refs.bib` from `paper/refs.bib` (1816 bytes)
- `latex/colm2026_conference.sty` from `paper/colm2026_conference.sty` (7727 bytes)
- `latex/colm2026_conference.bst` from `paper/colm2026_conference.bst` (26973 bytes)
- `latex/fancyhdr.sty` from `paper/fancyhdr.sty` (20521 bytes)
- `latex/natbib.sty` from `paper/natbib.sty` (45154 bytes)
- `latex/math_commands.tex` from `paper/math_commands.tex` (12284 bytes)
- `TEMPLATE_PROVENANCE.md` from `paper/TEMPLATE_PROVENANCE.md` (986 bytes)
