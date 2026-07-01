# Trusted by Proxy Completion Audit

Generated: 2026-06-28

This audit maps the original research plan and the follow-up plan to current
artifacts. It is intended to make the submission state checkable before upload.

## Original Research Plan Requirements

| Requirement | Status | Evidence |
|---|---|---|
| Focused source-laundering framing | Done | `paper/main.tex`, title, abstract, Sections 1-2 |
| At least 30 benign tasks and 30 injected variants | Done | `slambench/tasks/subtle_multidomain_50pairs_v2.jsonl`; 50 benign + 50 injected |
| At least 3 domains | Done | `paper/main.tex`, SLaMBench table; workspace, CRM, code review, travel, research |
| At least 4 payload classes | Done | `paper/main.tex`; five payload classes |
| Mock tools and no real external side effects | Done | `src/tools.py`; `paper/main.tex`, Threat Model and Ethics Statement |
| Deterministic scoring | Done | `src/scoring.py`; `tests/test_scoring.py`; `scripts/analyze_results.py` |
| Direct baseline and delegated condition | Done | `c0_single_direct`, `c2x_3agent_extractive_naive`; main table |
| At least two defenses | Done | source-preserving, capability-scoped, TraceGate |
| Main affordable-model sweep | Done | `gpt-5.4-nano` 50-pair sweep; raw logs under `outputs/raw_logs/` |
| Uncertainty artifacts | Retained outside simplified manuscript | Historical interval-note files are retained for auditability; the simplified manuscript reports point estimates only. |
| BSR, ASR, ATR, PDR, CNAS reported | Done | `paper/main.tex`, main table; generated tables |
| Qualitative traces available | Done | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md` |
| Clear limitations and ethics | Done | `paper/main.tex`, Limitations and Ethics Statement |
| Related work positioning | Done | `paper/main.tex`, Related Work |
| Venue style | Done | `paper/main.tex` and `paper/supplement.tex` use COLM 2026 submission style |
| Page-limit compliance | Done | Current main PDF is 7 pages total; body/ethics content fits within pages 1-6 and references begin on page 6. |

## Follow-up Plan Requirements

| Requirement | Status | Evidence |
|---|---|---|
| Current-model replication on `gpt-5.5`, 25-pair subset | Done | `paper/tables/followup_gpt55_25pairs_1200_core/RESULT_SUMMARY.md`; c0/c2x/c5x ASR 0% |
| Report c0 ASR, c2x ASR, ATR, c5x ASR, BSR, IUSR, PDR, and TraceGate blocks | Done | `paper/tables/followup_gpt55_25pairs_1200_core/main_results.md` |
| Interpret low-ASR current-model result transparently | Done | `paper/main.tex`, Model Dependence; `paper/tables/followup_gpt55_25pairs_1200_core/RESULT_SUMMARY.md` |
| Delegation-depth/topology ablation on 25-pair slice | Done | `paper/tables/followup_gpt54nano_25pairs_1200_topology/RESULT_SUMMARY.md` |
| Include c0, c1, c2, c2x, optional c2o | Done | Clean `gpt-5.4-nano` topology table includes all five |
| No-API mechanism trace audit over saved topology and defense runs | Done | `paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism/`, `paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism/` |
| Optional repeatability sweep on hard injected cases | Done | `paper/tables/followup_gpt54nano_repeatability_6inj_3runs/RESULT_SUMMARY.md`; c2x 8/18 repeated attacks, c0 2/18, TraceGate replay 0/18 |
| Optional non-email side-effect slice | Done, mixed/negative | `paper/tables/followup_gpt54nano_nonemail_3pairs/RESULT_SUMMARY.md`; c0 1/3 injected attacks, c2x 0/3, TraceGate replay 0/3 |
| Optional guard baseline | Done as replay baseline | `paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/RESULT_SUMMARY.md`; LLM guard replay ASR 0%, IUSR 72%, cost about $0.02 |
| Optional heterogeneous-agent composition | Done as tiny role diagnostic | `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/RESULT_SUMMARY.md`; all-nano c2x attacks 6/6 hard injected tasks, nano-reader/planner plus `gpt-5.5` executor attacks 0/6 |
| Same-scale defense comparison | Done with replay caveat | `paper/tables/followup_gpt54nano_25pairs_1200_defense/RESULT_SUMMARY.md`; c2x/c3/c4 raw runs plus c5x deterministic replay |
| Cost control under $20 | Done | Follow-up summaries record about $5.53 for `gpt-5.5` core, about $0.39 for clean `gpt-5.4-nano` follow-ups, $0.03 for repeatability, $0.01 for non-email, $0.02 for guard, and $0.26 for the canonical heterogeneous diagnostic; no API calls were needed for TraceGate replay |

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

## Current Verification Commands

```bash
conda run -n trusted_proxy python scripts/validate_tasks.py slambench/tasks/subtle_multidomain_50pairs_v2.jsonl
conda run -n trusted_proxy python scripts/validate_tasks.py slambench/tasks/subtle_multidomain_25pairs_v2.jsonl
conda run -n trusted_proxy python -m compileall src scripts tests
conda run -n trusted_proxy python -m unittest discover -s tests
conda run -n trusted_proxy python scripts/replay_tool_logs.py \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl \
  --out outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl
conda run -n trusted_proxy python scripts/replay_tool_logs.py \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl \
  --as-condition c5x_tracegate_extractive_naive \
  --out outputs/replayed_logs/followup_gpt54nano_25pairs_1200_defense_c5x_replay_from_c2x.jsonl
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c3.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c4.jsonl \
  outputs/replayed_logs/followup_gpt54nano_25pairs_1200_defense_c5x_replay_from_c2x.jsonl \
  --out-dir outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense \
  --tables-dir paper/tables/followup_gpt54nano_25pairs_1200_defense
conda run -n trusted_proxy python scripts/analyze_provenance_flow.py \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c1.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2o.jsonl \
  --out-dir outputs/analysis/followup_gpt54nano_25pairs_1200_topology_mechanism \
  --tables-dir paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism
conda run -n trusted_proxy python scripts/analyze_provenance_flow.py \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c3.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c4.jsonl \
  outputs/replayed_logs/followup_gpt54nano_25pairs_1200_defense_c5x_replay_from_c2x.jsonl \
  --out-dir outputs/analysis/followup_gpt54nano_25pairs_1200_defense_mechanism \
  --tables-dir paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/raw_logs/followup_gpt54nano_repeatability_6inj_c0_3runs.jsonl \
  outputs/raw_logs/followup_gpt54nano_repeatability_6inj_c2x_3runs.jsonl \
  outputs/replayed_logs/followup_gpt54nano_repeatability_6inj_c5x_replay_from_c2x_3runs.jsonl \
  --out-dir outputs/scored_runs/followup_gpt54nano_repeatability_6inj_3runs \
  --tables-dir paper/tables/followup_gpt54nano_repeatability_6inj_3runs
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/raw_logs/followup_gpt54nano_nonemail_3pairs_c0.jsonl \
  outputs/raw_logs/followup_gpt54nano_nonemail_3pairs_c2x.jsonl \
  outputs/replayed_logs/followup_gpt54nano_nonemail_3pairs_c5x_replay_from_c2x.jsonl \
  --out-dir outputs/scored_runs/followup_gpt54nano_nonemail_3pairs \
  --tables-dir paper/tables/followup_gpt54nano_nonemail_3pairs
conda run -n trusted_proxy python scripts/replay_with_llm_guard.py \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl \
  --model gpt-5.4-nano \
  --api-key-file "$OPENAI_API_KEY_FILE" \
  --max-output-tokens 700 \
  --resume \
  --out outputs/replayed_logs/followup_gpt54nano_25pairs_1200_guard_c6_from_c2x.jsonl
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c3.jsonl \
  outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c4.jsonl \
  outputs/replayed_logs/followup_gpt54nano_25pairs_1200_defense_c5x_replay_from_c2x.jsonl \
  outputs/replayed_logs/followup_gpt54nano_25pairs_1200_guard_c6_from_c2x.jsonl \
  --out-dir outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_guard \
  --tables-dir paper/tables/followup_gpt54nano_25pairs_1200_defense_guard
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x.jsonl \
  --out-dir outputs/scored_runs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x \
  --tables-dir paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x
make -C paper
conda run -n trusted_proxy python scripts/make_artifact_manifest.py
conda run -n trusted_proxy python scripts/make_submission_bundle.py
conda run -n trusted_proxy python scripts/check_paper_artifacts.py
```

The current main PDF is 7 pages total, with body/ethics content within pages
1-6 and references beginning on page 6. The supplement is 2 pages. The artifact
checker now also verifies manuscript numeric/caveat text against the saved
result package and checks that references do not begin before page 6. The latest
LaTeX log scan has only underfull hbox warnings and no unresolved
citations/references, overfull boxes, or listed LaTeX errors.

## Remaining Human Action

The research package is ready for a writing/review pass and satisfies the
recorded workshop rule of 6 pages excluding references. Before upload, confirm
that the chosen submission system uses the same page rule, then upload
`paper/main.pdf` and `paper/supplement.pdf`, or the assembled
`submission/trusted_by_proxy_submission_bundle.zip`.
