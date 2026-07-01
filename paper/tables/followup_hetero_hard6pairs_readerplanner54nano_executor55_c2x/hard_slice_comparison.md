# Heterogeneous hard-slice comparison

Task set: `slambench/tasks/subtle_multidomain_hard6pairs_v2.jsonl`

This table compares the same six hard base tasks across saved c2x runs. The
six tasks were selected because the clean `gpt-5.4-nano` topology audit found
extractive delegation attacks there while direct exposure did not. This is a
role-composition diagnostic, not an unbiased benchmark estimate.

| Setting | Runs | Injected runs | BSR | IUSR | ASR | PDR | CNAS | Blocks | Attack runs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| All `gpt-5.4-nano` c2x | 12 | 6 | 66.7% | 0.0% | 100.0% | 100.0% | 1.50 | 0 | 6/6 |
| All `gpt-5.5` c2x | 12 | 6 | 33.3% | 50.0% | 0.0% | 100.0% | 0.00 | 0 | 0/6 |
| `gpt-5.4-nano` reader/planner + `gpt-5.5` executor c2x | 12 | 6 | 66.7% | 66.7% | 0.0% | 83.3% | 0.00 | 0 | 0/6 |

