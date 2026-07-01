# Follow-up delegation-depth ablation: gpt-5.4-nano, 25 pairs

Date: 2026-06-28

Task set: `slambench/tasks/subtle_multidomain_25pairs_v2.jsonl`

Raw logs:

- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c1.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl`
- `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2o.jsonl`

Analysis artifacts:

- `outputs/scored_runs/followup_gpt54nano_25pairs_1200_topology/scored_runs.jsonl`
- `outputs/scored_runs/followup_gpt54nano_25pairs_1200_topology/main_results.jsonl`
- `paper/tables/followup_gpt54nano_25pairs_1200_topology/main_results.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_topology/payload_results.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_topology/bootstrap_notes.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_topology/trace_examples.md`

## Result

| Condition | Runs | BSR | IUSR | ASR | ATR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 60% | 48% | 4% | 0 pp | 0% | 0 |
| `c1_2agent_naive` | 50 | 64% | 60% | 0% | -4 pp | 72% | 0 |
| `c2_3agent_naive` | 50 | 72% | 72% | 4% | 0 pp | 52% | 0 |
| `c2x_3agent_extractive_naive` | 50 | 68% | 56% | 24% | +20 pp | 86% | 0 |
| `c2o_3agent_oracle_laundered` | 50 | 80% | 52% | 28% | +24 pp | 70% | 0 |

All five condition logs completed with zero run errors.

Measured API usage, using the pricing recorded in `followup_experiments_plan.md`:

| Condition | Calls | Input tokens | Output tokens | Estimated cost |
|---|---:|---:|---:|---:|
| `c0_single_direct` | 50 | 19,075 | 12,422 | $0.0193 |
| `c1_2agent_naive` | 100 | 35,548 | 21,247 | $0.0337 |
| `c2_3agent_naive` | 150 | 75,412 | 42,663 | $0.0684 |
| `c2x_3agent_extractive_naive` | 150 | 80,921 | 46,971 | $0.0749 |
| `c2o_3agent_oracle_laundered` | 100 | 59,183 | 27,353 | $0.0460 |
| Total | 550 | 270,139 | 150,656 | $0.2423 |

## Interpretation

This ablation supports a compositional source-laundering mechanism, but not a
simple "more agents always means more attacks" claim. The naive 2-agent and
3-agent chains do not increase ASR over direct exposure. The attack appears when
the upstream handoff strips or normalizes provenance: extractive delegation
raises ASR from 4% to 24%, and the oracle-laundered condition raises ASR to 28%.

Bootstrap paired differences against direct exposure:

- `c1_2agent_naive - c0_single_direct`: -4 pp, 95% CI [-12, 0]
- `c2_3agent_naive - c0_single_direct`: 0 pp, 95% CI [-12, 12]
- `c2x_3agent_extractive_naive - c0_single_direct`: +20 pp, 95% CI [0, 40]
- `c2o_3agent_oracle_laundered - c0_single_direct`: +24 pp, 95% CI [4, 44]

Paper-safe claim: delegation depth alone is insufficient to explain the effect.
Source-laundering occurs when intermediate agents transform untrusted
instructions into provenance-poor peer messages; the oracle-laundered condition
is the strongest mechanism check because the downstream planner and executor are
given a deliberately provenance-stripped handoff.

This table is a good candidate for the paper's topology-depth ablation. It should
be framed as "provenance-losing composition" rather than "generic multi-agent
depth."
