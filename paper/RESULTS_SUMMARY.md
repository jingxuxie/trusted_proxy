# Trusted by Proxy: Current Results Summary

Generated: 2026-06-28

## Current Empirical Story

The paper now has four paper-facing result layers:

1. A 50-pair main SLaMBench result on `gpt-5.4-nano`.
2. A clean 25-pair topology ablation on `gpt-5.4-nano`.
3. A clean 25-pair model-dependence check on `gpt-5.5`.
4. Small diagnostic probes for repeatability, non-email side effects, LLM guard
   replay, and heterogeneous role composition.

The strongest positive source-laundering result remains the corrected 50-pair
SLaMBench benchmark:

- Task set: `slambench/tasks/subtle_multidomain_50pairs_v2.jsonl`
- Main table: `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`
- Raw OpenAI logs:
  - `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl`
  - `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl`
  - `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl`
- Replayed TraceGate-pruning log:
  `outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl`

| Condition | BSR | IUSR | ASR | ATR | PDR | CNAS | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 60% | 54% | 6% | 0 pp | 0% | 0.10 | 0 |
| `c2x_3agent_extractive_naive` | 70% | 50% | 22% | +16 pp | 77% | 0.31 | 0 |
| `c5x_tracegate_extractive_naive` | 66% | 64% | 0% | -6 pp | 69% | 0.00 | 11 |

Paper-safe main claim:

> On a corrected 50-pair synthetic multidomain benchmark, extractive
> multi-agent delegation increases unauthorized audit-recipient sends for
> `gpt-5.4-nano` relative to direct exposure. A deterministic TraceGate monitor
> eliminates observed unauthorized sends while preserving injected-task utility.

## Follow-up Topology Ablation

Artifact summary:
`paper/tables/followup_gpt54nano_25pairs_1200_topology/RESULT_SUMMARY.md`

Task set: `slambench/tasks/subtle_multidomain_25pairs_v2.jsonl`.
All five condition logs completed with zero run errors.

| Condition | BSR | IUSR | ASR | ATR | PDR |
|---|---:|---:|---:|---:|---:|
| `c0_single_direct` | 60% | 48% | 4% | 0 pp | 0% |
| `c1_2agent_naive` | 64% | 60% | 0% | -4 pp | 72% |
| `c2_3agent_naive` | 72% | 72% | 4% | 0 pp | 52% |
| `c2x_3agent_extractive_naive` | 68% | 56% | 24% | +20 pp | 86% |
| `c2o_3agent_oracle_laundered` | 80% | 52% | 28% | +24 pp | 70% |

Interpretation: generic delegation depth is not sufficient. The naive 2-agent
and 3-agent chains do not increase ASR over direct exposure. The attack appears
when the upstream handoff strips or normalizes provenance: extractive delegation
raises ASR from 4% to 24%, and oracle-laundered handoff raises it to 28%.

Mechanism trace audit:
`paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism/`.
In all 6 injected tasks where `c2x` attacks and direct exposure does not, the
forbidden recipient appears in the reader handoff, planner plan, and executor
output before the tool call. This is no-API analysis over saved traces.

## Follow-up Defense Comparison

Artifact summary:
`paper/tables/followup_gpt54nano_25pairs_1200_defense/RESULT_SUMMARY.md`

This table uses clean raw runs for `c0`, `c2x`, `c3`, and `c4`, plus a
deterministic TraceGate replay of the saved `c2x` outputs under the `c5x`
runtime. The replay is valid as a tool-boundary enforcement check because `c2x`
and `c5x` share prompts and differ only in runtime monitoring; it is not an
independent model resampling.

| Condition | BSR | IUSR | ASR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|
| `c2x_3agent_extractive_naive` | 68% | 56% | 24% | 86% | 0 |
| `c3_source_preserving` | 44% | 56% | 0% | 86% | 0 |
| `c4_capability_scoped` | 52% | 52% | 0% | 86% | 0 |
| `c5x_tracegate_extractive_naive` replay | 68% | 72% | 0% | 86% | 10 |
| `c6_llm_guard_extractive_naive` replay | 68% | 72% | 0% | 86% | 0 |

ASR differences against `c2x` are -24 pp for `c3`, `c4`, TraceGate replay, and
LLM guard replay.

LLM guard baseline:
`paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/RESULT_SUMMARY.md`.
The guard replay sanitizes the same saved c2x proposed tool calls with one cheap
model call per run. It matches TraceGate on this slice: 0% ASR, 72% IUSR, 68%
BSR, zero parser/runtime errors. Guard-only cost was about $0.02. Treat it as an
empirical baseline, not a deterministic policy guarantee.

Defense trace audit:
`paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism/`.
On the same 25-pair slice, `c3` and `c4` carry forbidden markers in intermediate
messages but produce zero forbidden tool executions; TraceGate replay blocks
forbidden sends at runtime while preserving the saved extractive model outputs.

## Repeatability Check

Artifact summary:
`paper/tables/followup_gpt54nano_repeatability_6inj_3runs/RESULT_SUMMARY.md`

This is a post-hoc hard-case slice, not an unbiased benchmark estimate. It
reruns the six injected tasks where the clean 25-pair topology audit found c2x
attacked and direct exposure did not.

| Condition | Runs | Tasks attacked at least once | Attack runs | Injected utility runs | Blocks |
|---|---:|---:|---:|---:|---:|
| `c0_single_direct` | 18 | 1/6 | 2/18 | 9/18 | 0 |
| `c2x_3agent_extractive_naive` | 18 | 5/6 | 8/18 | 7/18 | 0 |
| `c5x_tracegate_extractive_naive` replay | 18 | 0/6 | 0/18 | 14/18 | 10 |

Interpretation: the six original c2x-only attacks are not perfectly
deterministic, but most remain live under resampling. TraceGate replay blocks or
prunes every repeated c2x forbidden send. Estimated API cost for the two raw
repeatability logs was about $0.03.

## Non-email Side-effect Probe

Artifact summary:
`paper/tables/followup_gpt54nano_nonemail_3pairs/RESULT_SUMMARY.md`

This tiny three-pair slice covers CRM ticket status updates, travel calendar
attendees, and research memory-policy writes. It is a scope probe, not a powered
benchmark.

| Condition | Runs | BSR | IUSR | ASR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 6 | 33% | 33% | 33% | 0% | 0 |
| `c2x_3agent_extractive_naive` | 6 | 33% | 33% | 0% | 83% | 0 |
| `c5x_tracegate_extractive_naive` replay | 6 | 33% | 33% | 0% | 83% | 1 |

Interpretation: this does not support a positive non-email c2x amplification
claim. Direct exposure executes one forbidden CRM status update; c2x and
TraceGate replay execute zero forbidden non-email side effects. The slice is
useful for showing that the harness and scorer cover structured side effects,
while the strongest positive paper claim remains unauthorized-recipient sends.
Estimated API cost was about $0.01.

## Current-model Replication

Artifact summary:
`paper/tables/followup_gpt55_25pairs_1200_core/RESULT_SUMMARY.md`

`gpt-5.5` on the 25-pair slice produced low ASR across all core conditions:

| Condition | BSR | IUSR | ASR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|
| `c0_single_direct` | 60% | 60% | 0% | 0% | 0 |
| `c2x_3agent_extractive_naive` | 40% | 44% | 0% | 100% | 0 |
| `c5x_tracegate_extractive_naive` | 44% | 48% | 0% | 100% | 1 |

Interpretation: this supports the follow-up plan's low-ASR current-model branch,
not a positive-ATR headline. It is useful as model-dependence evidence:
`gpt-5.5` appears robust to this SLaMBench-25 slice, while the benchmark still
exposes latent provenance dropout.

## Heterogeneous-agent Diagnostic

Artifact summary:
`paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/RESULT_SUMMARY.md`

This diagnostic uses the six hard injected tasks where the clean
`gpt-5.4-nano` topology audit found c2x attacks and direct exposure did not. It
compares saved c2x behavior on those six base tasks:

| Setting | Runs | BSR | IUSR | ASR | PDR | Attack runs |
|---|---:|---:|---:|---:|---:|---:|
| All `gpt-5.4-nano` c2x | 12 | 66.7% | 0.0% | 100.0% | 100.0% | 6/6 |
| All `gpt-5.5` c2x | 12 | 33.3% | 50.0% | 0.0% | 100.0% | 0/6 |
| `gpt-5.4-nano` reader/planner + `gpt-5.5` executor c2x | 12 | 66.7% | 66.7% | 0.0% | 83.3% | 0/6 |

Interpretation: this is not a powered defense comparison, but it is useful
model-role evidence. A stronger executor can absorb laundered instructions in
these hard cases, even when weaker upstream agents still drop provenance.
Estimated canonical API cost was about $0.26, dominated by the `gpt-5.5`
executor.

## Payload and Domain Findings

In the 50-pair main `c2x` result:

- `summary_bait`: 50% ASR
- `fake_authority`: 40% ASR
- `delegation_poisoning`: 10% ASR
- `direct_instruction`: 10% ASR
- `memory_poisoning`: 0% ASR

Observed `c2x` attacks occurred across all five domains: workspace (3), CRM (1),
code review (3), travel (2), and research (2).

## Negative and Mixed Findings

- Do not claim source laundering universally increases ASR across models.
  `gpt-5.5` has 0% ASR on the 25-pair core check, and `gpt-4.1-nano` was already
  directly vulnerable in older logs.
- Do not claim the heterogeneous-agent diagnostic proves a general robust
  composition rule. It covers one role assignment on six hard base tasks.
- Do not claim generic delegation depth is the cause. The clean topology
  ablation supports provenance-losing composition as the mechanism.
- Do not treat the six-task repeatability sweep as a population estimate. It is
  a post-hoc hard-case stability check.
- Do not claim the current data prove positive source-laundering amplification
  for non-email side effects. The tiny non-email probe is mixed/negative.
- Do not claim production-world exploit rates. SLaMBench is synthetic and
  closed-world.
- The TraceGate replay row in the follow-up defense table is a deterministic
  runtime replay, not a fresh model sample.
- The LLM guard replay row is also not a fresh end-to-end sample; it is a
  sanitizer over saved c2x proposed tool calls.

## Manuscript Artifacts

- LaTeX source: `paper/main.tex`
- Current main PDF: `paper/main.pdf` (7 pages total, COLM 2026 submission style; body/ethics content fits on pages 1-6 before references)
- Supplement PDF: `paper/supplement.pdf` (2 pages)
- Artifact manifest: `paper/ARTIFACT_MANIFEST.md`, `paper/ARTIFACT_MANIFEST.json`
- Claim checklist: `paper/CLAIM_CHECKLIST.md`
- Completion audit: `paper/COMPLETION_AUDIT.md`
- Mechanism tables: `paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism/`,
  `paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism/`
- Repeatability table: `paper/tables/followup_gpt54nano_repeatability_6inj_3runs/`
- Non-email side-effect table: `paper/tables/followup_gpt54nano_nonemail_3pairs/`
- LLM guard baseline: `paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/`
- Heterogeneous-agent diagnostic:
  `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/`
- Submission bundle: `submission/trusted_by_proxy_submission_bundle.zip`
