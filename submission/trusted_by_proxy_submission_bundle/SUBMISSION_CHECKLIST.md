# Trusted by Proxy Submission Checklist

Generated: 2026-06-28

## Current Submission Package

- Paper source: `paper/main.tex`
- Compiled draft: `paper/main.pdf`
- Supplement source: `paper/supplement.tex`
- Compiled supplement: `paper/supplement.pdf`
- Bibliography: `paper/refs.bib`
- Main result table: `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`
- Follow-up topology table: `paper/tables/followup_gpt54nano_25pairs_1200_topology/main_results.md`
- Follow-up defense table: `paper/tables/followup_gpt54nano_25pairs_1200_defense/main_results.md`
- Follow-up current-model table: `paper/tables/followup_gpt55_25pairs_1200_core/main_results.md`
- Heterogeneous diagnostic table: `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/main_results.md`
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
| Topology ablation documented | Done | `paper/main.tex`, Topology Ablation; `paper/tables/followup_gpt54nano_25pairs_1200_topology/RESULT_SUMMARY.md` |
| Defense ablation documented | Done | `paper/main.tex`, Defense Ablations; `paper/tables/followup_gpt54nano_25pairs_1200_defense/RESULT_SUMMARY.md` |
| Cross-model/current-model limitation documented | Done | `paper/main.tex`, Model Dependence |
| Heterogeneous-agent diagnostic documented | Done | `paper/main.tex`, Model Dependence; `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/RESULT_SUMMARY.md` |
| Deterministic replay/scoring documented | Done | `paper/supplement.tex` |
| Qualitative traces available | Done | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md` |
| Related work positioning | Done | `paper/main.tex`, Section 9 |
| Formal source-laundering definition | Done | `paper/main.tex`, Section 2 |
| Responsible release statement | Done | `paper/main.tex`, Ethics Statement |
| Submission artifact invariants checked | Done | `scripts/check_paper_artifacts.py`; includes result metrics, manuscript numeric/caveat text, PDF page counts, reference-page boundary, bundle freshness, and release redaction |
| Artifact hashes recorded | Done | `paper/ARTIFACT_MANIFEST.json` |
| Anonymous upload bundle assembled | Done | `submission/trusted_by_proxy_submission_bundle.zip` |
| Requirement-level completion audit | Done | `paper/COMPLETION_AUDIT.md` |
| Venue template conversion | Done | `paper/main.tex` and `paper/supplement.tex` use `colm2026_conference`; style files are vendored from the `Template-2026.zip` archive recorded in `paper/TEMPLATE_PROVENANCE.md` |
| 6-page excluding-references page rule | Done | `paper/main.pdf` is 7 pages total; the main body and ethics statement fit within pages 1-6, and references begin on page 6. `paper/supplement.pdf` is 2 pages. |

## Venue Rules Verified

- Target page: `https://advml-frontier.github.io/`
- Template source: `Template-2026.zip` (`sha256 24c616f7c37769db12fb2f2064b0f55a710b1503d673ba6a3cc114c54c01335e`)
- Verified on 2026-06-28 for the earlier workshop target: submissions use the COLM 2026 template; workshop papers are up to 6 pages excluding references and supplementary material; deadline is June 30, 2026 AoE.
- Current follow-up package: `paper/main.pdf` is 7 pages total under the COLM submission style; body/ethics content fits within pages 1-6 and references begin on page 6. `paper/supplement.pdf` is 2 pages.

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
- Do not claim the heterogeneous-agent diagnostic proves a general robust composition rule.
- Do not claim prompt-only defenses are sufficient.
- Do not claim SLaMBench estimates production-world exploit rates.
- Do not describe TraceGate's 11 blocks as all malicious: one block is a benign CRM memory-write false positive.
- Do not use PDR values from historical table directories unless they were regenerated after the task-specific PDR scorer fix. The paper's PDR claims use `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`.
