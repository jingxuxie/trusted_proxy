# Trusted by Proxy Completion Audit

Generated: 2026-06-28

This audit maps the original research-plan requirements to current artifacts.
It is intended to make the submission state checkable before upload.

## Research Plan Requirements

| Requirement | Status | Evidence |
|---|---|---|
| Focused source-laundering framing | Done | `paper/main.tex`, title, abstract, Sections 1-2 |
| At least 30 benign tasks and 30 injected variants | Done | `slambench/tasks/subtle_multidomain_50pairs_v2.jsonl`; 50 benign + 50 injected |
| At least 3 domains | Done | `paper/main.tex`, Table 1; workspace, CRM, code review, travel, research |
| At least 4 payload classes | Done | `paper/main.tex`, Section 3; direct instruction, fake authority, delegation poisoning, summary bait, memory poisoning |
| Mock tools and no real external side effects | Done | `src/tools.py`; `paper/main.tex`, Threat Model and Ethics Statement |
| Deterministic scoring | Done | `src/scoring.py`; `tests/test_scoring.py`; `scripts/analyze_results.py` |
| Single-agent direct baseline | Done | `c0_single_direct`; `paper/main.tex`, Table 2 |
| Multi-agent delegated condition | Done | `c2x_3agent_extractive_naive`; `paper/main.tex`, Table 2 |
| At least two defenses | Done | source-preserving, capability-scoped, TraceGate; `paper/main.tex`, Table 4 |
| Main affordable-model sweep | Done | `gpt-5.4-nano` 50-pair sweep; raw logs under `outputs/raw_logs/` |
| Cross-model or stronger-model subset | Done | `gpt-4.1-nano` 25-pair subset; `paper/main.tex`, Table 5 |
| Confidence intervals or bootstrap intervals | Done | `paper/main.tex`, Section 6; `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/bootstrap_notes.md` |
| BSR, ASR, ATR, PDR, CNAS reported | Done | `paper/main.tex`, Table 2; `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md` |
| Qualitative traces available | Done | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md`; `paper/supplement.tex` |
| Clear limitations and ethics | Done | `paper/main.tex`, Limitations and Ethics Statement |
| Related work distinguishes key prior work | Done | `paper/main.tex`, Section 9 |
| Venue style and page limit | Done | `paper/main.pdf` is 5 pages under COLM 2026 submission style rebased from `/home/eston/colm_workshop/Template-2026.zip`; `paper/supplement.pdf` is 2 pages |
| Anonymous submission package | Done | `submission/trusted_by_proxy_submission_bundle.zip` |

## Main Claim Evidence

The paper-safe main claim is:

> On a corrected 50-pair synthetic multidomain benchmark, extractive
> multi-agent delegation increases unauthorized audit-recipient sends for
> `gpt-5.4-nano` relative to direct exposure. A deterministic TraceGate monitor
> eliminates observed audit-recipient sends while preserving injected-task
> utility.

Current metric evidence:

| Condition | BSR | IUSR | ASR | ATR | PDR | CNAS | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 60% | 54% | 6% | 0 pp | 0% | 0.10 | 0 |
| `c2x_3agent_extractive_naive` | 70% | 50% | 22% | +16 pp | 77% | 0.31 | 0 |
| `c5x_tracegate_extractive_naive` | 66% | 64% | 0% | -6 pp | 69% | 0.00 | 11 |

## Verification Commands Run

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

All checks passed in the final verification pass. The LaTeX log scan showed no
overfull boxes, undefined citations, rerun warnings, or natbib errors; only
underfull spacing warnings remain.

## Remaining Human Action

The research package is ready for submission. The remaining action is external:
upload `paper/main.pdf` and `paper/supplement.pdf`, or the assembled
`submission/trusted_by_proxy_submission_bundle.zip`, to the target submission
system.
