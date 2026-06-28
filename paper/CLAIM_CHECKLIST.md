# Trusted by Proxy Claim Checklist

Generated: 2026-06-28

## Supported Main Claims

| Claim | Status | Evidence | Notes |
|---|---|---|---|
| Extractive multi-agent delegation increases unauthorized-recipient sends relative to direct exposure on the main `gpt-5.4-nano` benchmark. | Supported | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`; c0 ASR 6%, c2x ASR 22%, paired bootstrap CI [4, 26] pp. | This is the central source-laundering result. |
| Extractive delegation frequently drops provenance before execution. | Supported | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`; c2x PDR 77%, c5x PDR 69%. | TraceGate blocks at the tool boundary; it does not repair upstream messages. |
| The attack effect appears across multiple domains, not only workspace/email. | Supported | `outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/scored_runs.jsonl`; c2x attacks in workspace, CRM, code review, travel, and research. | Counts: workspace 3, CRM 1, code review 3, travel 2, research 2. |
| TraceGate eliminates observed unauthorized audit-recipient sends on the scaled benchmark. | Supported | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/attack_reason_results.md`; c5x has no attack-reason rows and 0 audit sends in replayed logs. | TraceGate recorded 11 sensitive-call blocks: 10 on injected variants and one benign memory-write false positive. |
| TraceGate preserves injected-task utility better than the vulnerable c2x system on the scaled benchmark. | Supported | `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`; c2x IUSR 50%, c5x IUSR 64%. | This relies on deterministic recipient pruning replay from saved model outputs. |
| Source-preserving prompting removes observed attacks on the 25-pair `gpt-5.4-nano` benchmark but reduces utility. | Supported on 25-pair run | `paper/tables/openai_schema_prompt_v2b_gpt54nano/main_results.md`; c3 BSR 44%, ASR 0%. | Do not present as scaled 50-pair evidence unless rerun. |
| Capability-scoped prompting is weaker than TraceGate in the current setup. | Supported on 25-pair run | `paper/tables/openai_schema_prompt_v2b_gpt54nano/main_results.md`; c4 BSR 40%, strict ASR 4%, c5x BSR 72%, ASR 0%. | c4 had no audit sends but one strict synthetic-secret identifier failure. |

## Mixed or Unsupported Claims

| Claim | Status | Evidence | Required wording |
|---|---|---|---|
| Source laundering universally increases attack success across models. | Not supported | `paper/tables/schema_prompt_v2b_cross_model.md`; `gpt-4.1-nano` c0 ASR 24%, c2x ASR 24%. | Say the delegation-specific lift is model-dependent. |
| `gpt-4.1-nano` is safer than `gpt-5.4-nano`. | Not supported | Direct ASR is higher on `gpt-4.1-nano`; BSR is lower. | Say `gpt-4.1-nano` is directly vulnerable and less useful in this benchmark. |
| Prompt-only defenses are sufficient. | Not supported | c3 and c4 reduce attacks but reduce BSR; c3 still fails on `gpt-4.1-nano`. | Say prompt-only defenses help but are brittle. |
| Results establish production-world attack rates. | Not supported | All tasks and tools are synthetic mocks. | Say SLaMBench is a controlled systems benchmark, not a production prevalence study. |

## Paper-Safe Claim Wording

Use:

> On a scaled synthetic multidomain benchmark, source-laundering through extractive delegation increases unauthorized-recipient tool calls for `gpt-5.4-nano`; a deterministic runtime monitor eliminates observed unauthorized sends while preserving injected-task utility.

Avoid:

> Multi-agent systems are always less safe than direct agents.

Avoid:

> Source preservation solves source laundering.

Avoid:

> The benchmark proves real-world exploitability rates.
