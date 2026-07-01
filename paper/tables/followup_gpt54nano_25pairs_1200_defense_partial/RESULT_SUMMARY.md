# Follow-up defense comparison: gpt-5.4-nano, 25 pairs, partial clean table

Date: 2026-06-28

Task set: `slambench/tasks/subtle_multidomain_25pairs_v2.jsonl`

Clean raw logs included:

- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c3.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c4.jsonl`

Pending clean row:

- `c5x_tracegate_extractive_naive`

The clean `c5x` rerun was not launched in this turn because the execution
approval layer returned a model-capacity rejection for the API command. Older
`gpt-5.4-nano` `c5x` logs exist, but they were produced with the earlier lower
output cap and contain parse/truncation errors, so they are intentionally not
mixed into this clean table.

Analysis artifacts:

- `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_partial/scored_runs.jsonl`
- `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_partial/main_results.jsonl`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense_partial/main_results.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense_partial/payload_results.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense_partial/bootstrap_notes.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense_partial/trace_examples.md`

## Result

| Condition | Runs | BSR | IUSR | ASR | ATR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 60% | 48% | 4% | 0 pp | 0% | 0 |
| `c2x_3agent_extractive_naive` | 50 | 68% | 56% | 24% | +20 pp | 86% | 0 |
| `c3_source_preserving` | 50 | 44% | 56% | 0% | -4 pp | 86% | 0 |
| `c4_capability_scoped` | 50 | 52% | 52% | 0% | -4 pp | 86% | 0 |

All included logs completed with zero run errors.

Measured API usage for included logs, using the pricing recorded in
`followup_experiments_plan.md`:

| Condition | Calls | Input tokens | Output tokens | Estimated cost |
|---|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 19,075 | 12,422 | $0.0193 |
| `c2x_3agent_extractive_naive` | 150 | 80,921 | 46,971 | $0.0749 |
| `c3_source_preserving` | 150 | 96,873 | 49,437 | $0.0812 |
| `c4_capability_scoped` | 150 | 78,451 | 44,163 | $0.0709 |
| Total | 500 | 275,320 | 152,993 | $0.2463 |

## Interpretation

This partial defense table is already paper-useful: on the same 25-pair slice
where extractive source-laundering reaches 24% ASR, both source-preserving
delegation and capability-scoped delegation reduce ASR to 0%.

Paired bootstrap differences against extractive delegation:

- `c3_source_preserving - c2x_3agent_extractive_naive`: -24 pp, 95% CI [-40, -8]
- `c4_capability_scoped - c2x_3agent_extractive_naive`: -24 pp, 95% CI [-40, -8]

Paper-safe claim: explicit provenance preservation and capability-scoped
authorization both prevent observed forbidden tool execution on this clean
SLaMBench-25 slice. The table should be labeled partial until the clean
TraceGate row is added.
