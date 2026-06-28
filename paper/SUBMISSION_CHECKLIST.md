# Trusted by Proxy Submission Checklist

Generated: 2026-06-28

## Current Submission Package

- Paper source: `paper/main.tex`
- Compiled draft: `paper/main.pdf`
- Supplement source: `paper/supplement.tex`
- Compiled supplement: `paper/supplement.pdf`
- Bibliography: `paper/refs.bib`
- Main result table: `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`
- Artifact manifest: `paper/ARTIFACT_MANIFEST.md`, `paper/ARTIFACT_MANIFEST.json`
- Submission bundle: `submission/trusted_by_proxy_submission_bundle.zip`
- Template provenance: `paper/TEMPLATE_PROVENANCE.md`
- Claim boundary file: `paper/CLAIM_CHECKLIST.md`
- Result summary: `paper/RESULTS_SUMMARY.md`
- Completion audit: `paper/COMPLETION_AUDIT.md`
- Regression tests: `tests/test_scoring.py`

## Evidence Status

| Requirement | Status | Evidence |
|---|---|---|
| Threat model for source laundering | Done | `paper/main.tex`, Sections 1-2 |
| SLaMBench benchmark description | Done | `paper/main.tex`, Section 3; `slambench/tasks/subtle_multidomain_50pairs_v2.jsonl` |
| Direct-vs-delegated comparison | Done | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md` |
| Authority Transfer Rate reported | Done | `paper/main.tex`, Table 2 |
| Provenance dropout measured | Done | `paper/main.tex`, Table 2; c2x PDR 77%, c5x PDR 69% |
| Lightweight defense evaluated | Done | TraceGate result in `paper/main.tex`, Table 2 |
| Cross-model limitation documented | Done | `paper/main.tex`, Section 8 |
| Deterministic replay/scoring documented | Done | `paper/supplement.tex` |
| Qualitative traces available | Done | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md` |
| Related work positioning | Done | `paper/main.tex`, Section 9 |
| Formal source-laundering definition | Done | `paper/main.tex`, Section 2 |
| Responsible release statement | Done | `paper/main.tex`, Ethics Statement |
| Submission artifact invariants checked | Done | `scripts/check_paper_artifacts.py` |
| Artifact hashes recorded | Done | `paper/ARTIFACT_MANIFEST.json` |
| Anonymous upload bundle assembled | Done | `submission/trusted_by_proxy_submission_bundle.zip` |
| Requirement-level completion audit | Done | `paper/COMPLETION_AUDIT.md` |
| Venue template conversion | Done | `paper/main.tex` and `paper/supplement.tex` use `colm2026_conference`; style files are vendored from `/home/eston/colm_workshop/Template-2026.zip` |
| Page-rule decision for supplement | Done | Workshop page permits supplementary material outside the 6-page limit; supplement is separate in `paper/supplement.pdf` |

## Venue Rules Verified

- Target page: `https://advml-frontier.github.io/`
- Template source: `/home/eston/colm_workshop/Template-2026.zip` (`sha256 24c616f7c37769db12fb2f2064b0f55a710b1503d673ba6a3cc114c54c01335e`)
- Verified on 2026-06-28: submissions use the COLM 2026 template; workshop papers are up to 6 pages excluding references and supplementary material; deadline is June 30, 2026 AoE.
- Current package: `paper/main.pdf` is 5 pages under the COLM submission style, and `paper/supplement.pdf` is 2 pages.

## Commands To Verify Before Submission

```bash
conda run -n trusted_proxy python scripts/validate_tasks.py slambench/tasks/subtle_multidomain_50pairs_v2.jsonl
conda run -n trusted_proxy python -m compileall src scripts tests
conda run -n trusted_proxy python -m unittest discover -s tests
conda run -n trusted_proxy python scripts/replay_tool_logs.py \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl \
  --out outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl \
  --out-dir outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned \
  --tables-dir paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned
make -C paper
conda run -n trusted_proxy python scripts/make_artifact_manifest.py
conda run -n trusted_proxy python scripts/make_submission_bundle.py
conda run -n trusted_proxy python scripts/check_paper_artifacts.py
```

## Paper-Safe Main Claim

On a corrected 50-pair synthetic multidomain benchmark, extractive multi-agent
delegation increases unauthorized audit-recipient sends for `gpt-5.4-nano`
relative to direct exposure. A deterministic TraceGate monitor eliminates
observed audit-recipient sends while preserving injected-task utility.
The intermediate-message PDR result supports the mechanism claim: extractive
delegation often carries forbidden recipient content without source and
authority metadata, while TraceGate blocks at the tool boundary.

## Claims To Avoid

- Do not claim source laundering universally increases attack success across all models.
- Do not claim prompt-only defenses are sufficient.
- Do not claim SLaMBench estimates production-world exploit rates.
- Do not describe TraceGate's 11 blocks as all malicious: one block is a benign CRM memory-write false positive.
- Do not use PDR values from historical table directories unless they were regenerated after the task-specific PDR scorer fix. The paper's PDR claims use `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`.
