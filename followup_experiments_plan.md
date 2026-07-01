# Follow-up experiment plan

This plan strengthens the source-laundering paper with a small number of API-only experiments.

## Execution status

Status as of 2026-06-28: the minimum experiments are complete, and all optional
additions below have at least a bounded diagnostic artifact. The current
paper-facing package uses:

- `gpt-5.5` current-model replication on the 25-pair core slice.
- `gpt-5.4-nano` topology ablation on the 25-pair slice.
- `gpt-5.4-nano` defense comparison with TraceGate replay and an LLM-guard
  replay baseline.
- Post-hoc repeatability, tiny non-email side-effect, and tiny heterogeneous
  role-composition diagnostics.

The authoritative current write-up is `paper/main.tex`; claim boundaries are in
`paper/CLAIM_CHECKLIST.md`, and requirement-level evidence is in
`paper/COMPLETION_AUDIT.md`.

## Minimum experiments

### 1. Current-model replication

Run the core three conditions on `gpt-5.5` using a 25-pair subset first, then expand to the full 50-pair set only if the measured API cost is acceptable.

Conditions:

- `c0_single_direct`
- `c2x_3agent_extractive_naive`
- `c5x_tracegate_extractive_naive`

Report c0 ASR, c2x ASR, ATR, c5x ASR, BSR, IUSR, PDR, and TraceGate block counts.

Interpretation:

- Positive ATR on `gpt-5.5`: headline cross-model support.
- High direct ASR but low ATR: model-level direct susceptibility dominates, but TraceGate remains useful.
- Low ASR across all conditions: report as a robustness result and keep SLaMBench as a diagnostic benchmark.

### 2. Delegation-depth ablation

Run a 25-pair topology sweep to show that the phenomenon is compositional rather than only prompt-specific.

Conditions:

- `c0_single_direct`
- `c1_2agent_naive`
- `c2_3agent_naive`
- `c2x_3agent_extractive_naive`
- optional: `c2o_3agent_oracle_laundered`

Report ASR, IUSR, and PDR as a function of delegation topology.

### 3. Same-scale defense comparison

Expand the defense comparison beyond the current 25-pair pilot if budget permits.

Conditions:

- `c2x_3agent_extractive_naive`
- `c3_source_preserving`
- `c4_capability_scoped`
- `c5x_tracegate_extractive_naive`

Prefer the full SLaMBench-50 set on `gpt-5.4-nano` or `gpt-5.4-mini`. This is cheaper than using `gpt-5.5` for every ablation.

## Optional high-impact additions

1. Heterogeneous-agent composition: mix cheap and strong models across Reader, Planner, and Executor roles.
2. Non-email side-effect slice: add a small set of state-changing tasks such as ticket updates, calendar attendees, and memory writes.
3. Repeatability sweep: rerun 10 hard injected cases three times to estimate per-case stability.
4. Guard baseline: add one LLM-based sanitizer and compare it with TraceGate.

## Cost-control strategy

Use `gpt-5.5` only for the core replication. Use cheaper models for topology and defense sweeps. Before running a full sweep, run a tiny pilot, inspect API usage, and extrapolate.

Cost formula:

```text
estimated_cost = input_million_tokens * input_price + output_million_tokens * output_price
```

The experiment summaries use the planning-time price assumptions recorded in
`scripts/summarize_openai_usage.py`: standard `gpt-5.5` at $5 per 1M input
tokens and $30 per 1M output tokens, and `gpt-5.4-nano` at $0.20 per 1M input
tokens and $1.25 per 1M output tokens. These prices are configurable because
provider pricing can change independently of saved artifacts.

## Paper update guidance

If the `gpt-5.5` replication supports positive ATR, add it to the main results as current-model support. If it does not, report the result transparently as model dependence and emphasize that TraceGate blocks the forbidden tool side effect across models. The strongest final paper will have three clean tables: core model comparison, topology-depth ablation, and defense comparison.

Actual outcome: the `gpt-5.5` replication followed the low-ASR branch, so the
paper reports it as model-dependence evidence rather than a positive-ATR
headline. The final paper keeps three central tables (main result, topology, and
defense comparison) and folds current-model, repeatability, non-email, guard,
and heterogeneous-role findings into model-dependence, limitations, and artifact
summaries with conservative wording.
