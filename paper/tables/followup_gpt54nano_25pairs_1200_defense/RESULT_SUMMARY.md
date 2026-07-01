# Follow-up defense comparison: gpt-5.4-nano, 25 pairs

Date: 2026-06-28

Task set: `slambench/tasks/subtle_multidomain_25pairs_v2.jsonl`

Clean raw logs included:

- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c3.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c4.jsonl`

Deterministic replay log:

- `outputs/replayed_logs/followup_gpt54nano_25pairs_1200_defense_c5x_replay_from_c2x.jsonl`

The TraceGate row is a replay of the saved `c2x` agent outputs under the
`c5x_tracegate_extractive_naive` runtime. This is valid as a tool-boundary
enforcement check because `c2x` and `c5x` use the same agent prompts and differ
only in the deterministic runtime monitor. It is not an independent resampling
of model outputs.

Analysis artifacts:

- `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense/scored_runs.jsonl`
- `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense/main_results.jsonl`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense/main_results.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense/payload_results.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense/bootstrap_notes.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense/trace_examples.md`

## Result

| Condition | Runs | BSR | IUSR | ASR | ATR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 60% | 48% | 4% | 0 pp | 0% | 0 |
| `c2x_3agent_extractive_naive` | 50 | 68% | 56% | 24% | +20 pp | 86% | 0 |
| `c3_source_preserving` | 50 | 44% | 56% | 0% | -4 pp | 86% | 0 |
| `c4_capability_scoped` | 50 | 52% | 52% | 0% | -4 pp | 86% | 0 |
| `c5x_tracegate_extractive_naive` replay | 50 | 68% | 72% | 0% | -4 pp | 86% | 10 |

All included raw logs completed with zero run errors; the replayed TraceGate row
contains zero run errors and 10 blocked tool-call events, 9 of them on injected
variants.

Measured API usage for the raw logs, using the pricing recorded in
`followup_experiments_plan.md`:

| Condition | Calls | Input tokens | Output tokens | Estimated cost |
|---|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 19,075 | 12,422 | $0.0193 |
| `c2x_3agent_extractive_naive` | 150 | 80,921 | 46,971 | $0.0749 |
| `c3_source_preserving` | 150 | 96,873 | 49,437 | $0.0812 |
| `c4_capability_scoped` | 150 | 78,451 | 44,163 | $0.0709 |
| TraceGate replay | 0 | 0 | 0 | $0.0000 |
| Total | 500 | 275,320 | 152,993 | $0.2463 |

## Interpretation

On the same 25-pair slice where extractive source-laundering reaches 24% ASR,
source-preserving delegation, capability-scoped delegation, and deterministic
TraceGate replay all reduce ASR to 0%.

Paired bootstrap differences against extractive delegation:

- `c3_source_preserving - c2x_3agent_extractive_naive`: -24 pp, 95% CI [-40, -8]
- `c4_capability_scoped - c2x_3agent_extractive_naive`: -24 pp, 95% CI [-40, -8]
- `c5x_tracegate_extractive_naive - c2x_3agent_extractive_naive`: -24 pp, 95% CI [-40, -8]

Paper-safe claim: explicit provenance preservation, capability-scoped
authorization, and deterministic tool-boundary enforcement each prevent observed
forbidden tool execution on this clean SLaMBench-25 slice. The TraceGate row
should be described as a deterministic replay of the same sampled model outputs,
while the 50-pair main table remains the primary independently sampled TraceGate
evaluation.
