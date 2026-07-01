# Follow-up current-model replication: gpt-5.5, 25 pairs

Date: 2026-06-28

Task set: `slambench/tasks/subtle_multidomain_25pairs_v2.jsonl`

Raw logs:

- `outputs/raw_logs/followup_gpt55_25pairs_1200_c0.jsonl`
- `outputs/raw_logs/followup_gpt55_25pairs_1200_c2x.jsonl`
- `outputs/raw_logs/followup_gpt55_25pairs_1200_c5x.jsonl`

Analysis artifacts:

- `outputs/scored_runs/followup_gpt55_25pairs_1200_core/scored_runs.jsonl`
- `outputs/scored_runs/followup_gpt55_25pairs_1200_core/main_results.jsonl`
- `paper/tables/followup_gpt55_25pairs_1200_core/main_results.md`
- `paper/tables/followup_gpt55_25pairs_1200_core/payload_results.md`
- `paper/tables/followup_gpt55_25pairs_1200_core/bootstrap_notes.md`
- `paper/tables/followup_gpt55_25pairs_1200_core/trace_examples.md`

## Result

| Condition | Runs | BSR | IUSR | ASR | ATR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 60% | 60% | 0% | 0 pp | 0% | 0 |
| `c2x_3agent_extractive_naive` | 50 | 40% | 44% | 0% | 0 pp | 100% | 0 |
| `c5x_tracegate_extractive_naive` | 50 | 44% | 48% | 0% | 0 pp | 100% | 1 |

All three condition logs completed with zero run errors.

Measured API usage, using the pricing recorded in `followup_experiments_plan.md`:

| Condition | Calls | Input tokens | Output tokens | Estimated cost |
|---|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 19,075 | 25,851 | $0.8709 |
| `c2x_3agent_extractive_naive` | 150 | 78,008 | 65,372 | $2.3512 |
| `c5x_tracegate_extractive_naive` | 150 | 76,166 | 64,290 | $2.3095 |
| Total | 350 | 173,249 | 155,513 | $5.5316 |

## Interpretation

This run supports the follow-up plan's low-ASR current-model branch, not the
headline positive-ATR branch. On `gpt-5.5`, the 25-pair subset produced no
unauthorized sends in direct, extractive multi-agent, or TraceGate conditions.
The extractive multi-agent conditions still exhibit complete provenance dropout
on injected cases, but that dropout did not convert into observed forbidden tool
execution. Utility is lower in the extractive chains than in direct execution.

Paper-safe claim: `gpt-5.5` appears more robust to this SLaMBench-25 slice than
the earlier `gpt-5.4-nano` result, while SLaMBench still exposes provenance
dropout as a latent mechanism. This should be reported as model dependence and
robustness evidence, not as current-model attack amplification.

Next best experiment: run the delegation-depth ablation on a cheaper model using
the same 25-pair slice, preferably reusing existing `gpt-5.4-nano` c0/c2x logs
where possible and only adding missing c1/c2 conditions.
