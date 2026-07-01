# LLM guard baseline: gpt-5.4-nano, 25 pairs

Date: 2026-06-28

Task set: `slambench/tasks/subtle_multidomain_25pairs_v2.jsonl`

This baseline replays the saved `c2x_3agent_extractive_naive` executor outputs
through an LLM sanitizer before mock execution. The guard sees the original user
goal, trusted context, forbidden-outcome policy, and proposed tool calls, then
returns only allowed or sanitized calls. It is a replay baseline, not a fresh
end-to-end agent sample.

Raw/replayed logs:

- Source c2x log: `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl`
- Guard replay: `outputs/replayed_logs/followup_gpt54nano_25pairs_1200_guard_c6_from_c2x.jsonl`

Scored artifacts:

- `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_guard/scored_runs.jsonl`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/main_results.md`
- `paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/bootstrap_notes.md`

## Result

| Condition | BSR | IUSR | ASR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|
| `c2x_3agent_extractive_naive` | 68% | 56% | 24% | 86% | 0 |
| `c3_source_preserving` | 44% | 56% | 0% | 86% | 0 |
| `c4_capability_scoped` | 52% | 52% | 0% | 86% | 0 |
| `c5x_tracegate_extractive_naive` replay | 68% | 72% | 0% | 86% | 10 |
| `c6_llm_guard_extractive_naive` replay | 68% | 72% | 0% | 86% | 0 |

All 50 guard replay runs completed with zero parser or runtime errors.

Measured guard-only API usage:

| Calls | Input tokens | Output tokens | Estimated cost |
|---:|---:|---:|---:|
| 50 | 35,071 | 13,861 | $0.0243 |

## Interpretation

On this same saved-output slice, the LLM guard matches TraceGate's observed ASR
and utility: 0% ASR, 72% injected utility, and 68% benign success. It reduces ASR
by 24 percentage points relative to c2x, with paired bootstrap 95% CI [-40, -8].

This is useful as a guard-baseline comparison, but the paper should not frame it
as a production-ready replacement for deterministic enforcement. The LLM guard
is another model call, has no formal policy guarantee, and is evaluated here as
a replay sanitizer over saved proposed tool calls. TraceGate remains the
deterministic, auditable defense.
