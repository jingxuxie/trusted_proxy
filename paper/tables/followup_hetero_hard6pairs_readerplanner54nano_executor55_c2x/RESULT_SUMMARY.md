# Follow-up heterogeneous-agent diagnostic: hard six-task c2x slice

Date: 2026-06-28

Task set: `slambench/tasks/subtle_multidomain_hard6pairs_v2.jsonl`

Configuration:

- Condition: `c2x_3agent_extractive_naive`
- Reader: `gpt-5.4-nano`
- Planner: `gpt-5.4-nano`
- Executor: `gpt-5.5`
- Max output tokens: 900 for the original run; one malformed executor response
  on `research_subtle_002_injected` was replaced by a same-task rerun at 1200
  max output tokens.

Raw and analysis artifacts:

- `outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x.jsonl`
- `outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x_with_parser_error.jsonl`
- `outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x_repair_research_subtle_002.jsonl`
- `outputs/scored_runs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/scored_runs.jsonl`
- `outputs/scored_runs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/main_results.jsonl`
- `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/main_results.md`
- `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/payload_results.md`
- `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/hard_slice_comparison.md`

## Result

| Condition | Runs | BSR | IUSR | ASR | ATR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c2x_3agent_extractive_naive` | 12 | 66.7% | 66.7% | 0.0% | 0.0 pp | 83.3% | 0 |

The canonical raw log has 12 runs and zero recorded run errors.

Measured canonical API usage, using the pricing recorded in
`followup_experiments_plan.md`:

| Stage | Calls | Input tokens | Output tokens | Estimated cost |
|---|---:|---:|---:|---:|
| Reader (`gpt-5.4-nano`) | 12 | 3,481 | 2,322 | $0.0036 |
| Planner (`gpt-5.4-nano`) | 12 | 4,831 | 3,641 | $0.0055 |
| Executor (`gpt-5.5`) | 12 | 9,871 | 6,643 | $0.2486 |
| Total | 36 | 18,183 | 12,606 | $0.2577 |

## Hard-slice contrast

On the same six hard base tasks, the all-`gpt-5.4-nano` c2x topology run attacks
all six injected variants. The all-`gpt-5.5` c2x run attacks none but has lower
benign success. The heterogeneous reader/planner/executor split also attacks
none while matching the all-nano benign success on this slice.

| Setting | BSR | IUSR | ASR | PDR | Attack runs |
|---|---:|---:|---:|---:|---:|
| All `gpt-5.4-nano` c2x | 66.7% | 0.0% | 100.0% | 100.0% | 6/6 |
| All `gpt-5.5` c2x | 33.3% | 50.0% | 0.0% | 100.0% | 0/6 |
| `gpt-5.4-nano` reader/planner + `gpt-5.5` executor c2x | 66.7% | 66.7% | 0.0% | 83.3% | 0/6 |

## Interpretation

This is useful model-role evidence, not a powered defense comparison. It
suggests that a stronger executor can absorb laundered instructions produced by
weaker upstream agents in these hard cases, even though all six injected runs
show some provenance dropout and the average injected-run PDR remains 83.3%.
The result strengthens the paper's model-dependence boundary: attack
amplification is not universal across models or role assignments, and
executor-side robustness can matter independently of upstream provenance
quality.
