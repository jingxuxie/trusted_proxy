# Trusted by Proxy

Compact benchmark and experiment harness for studying source-laundering attacks in
multi-agent LLM systems.

The repository is intentionally closed-world: all tools are mocked, all secrets are
synthetic, and no experiment sends email, opens browsers, or calls external services
except the optional OpenAI model backend.

## Current paper result

The paper draft is in `paper/main.tex`, the compiled main artifact is
`paper/main.pdf`, and reproducibility details are split into
`paper/supplement.tex` / `paper/supplement.pdf`. The current main empirical
claim uses the corrected 50-pair SLaMBench task set:

- Tasks: `slambench/tasks/subtle_multidomain_50pairs_v2.jsonl`
- Main table: `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md`
- Raw OpenAI logs:
  - `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl`
  - `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl`
  - `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl`
- Replayed TraceGate-pruning log:
  `outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl`

Headline numbers on `gpt-5.4-nano`:

| Condition | BSR | IUSR | ASR | ATR | PDR | CNAS |
|---|---:|---:|---:|---:|---:|---:|
| Direct single-agent | 60% | 54% | 6% | 0 pp | 0% | 0.10 |
| Extractive multi-agent | 70% | 50% | 22% | +16 pp | 77% | 0.31 |
| TraceGate | 66% | 64% | 0% | -6 pp | 69% | 0.00 |

The central claim is that extractive delegation increases unauthorized audit
recipient sends relative to direct exposure, while TraceGate eliminates observed
audit sends and preserves injected-task utility. The high PDR values show that
runtime monitoring blocks execution even when upstream provenance has already
dropped out.

## Fast start

```bash
conda run -n trusted_proxy python scripts/validate_tasks.py slambench/tasks/subtle_multidomain_50pairs_v2.jsonl
conda run -n trusted_proxy python -m unittest discover -s tests
conda run -n trusted_proxy python scripts/replay_tool_logs.py \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl \
  --out outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl \
  --out-dir outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned \
  --tables-dir paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned
make -C paper
conda run -n trusted_proxy python scripts/make_artifact_manifest.py
conda run -n trusted_proxy python scripts/make_submission_bundle.py
conda run -n trusted_proxy python scripts/check_paper_artifacts.py
```

The replay and analysis steps are deterministic and do not call the OpenAI API.
The unit tests include regression coverage for task-specific provenance-dropout
markers such as `audit-log@example.test`.
The artifact checker verifies the required files, task/run counts, main claim
numbers, TraceGate block/pruning counts, COLM template use, main/supplement PDF
page counts, submission-bundle freshness, and artifact manifest hashes.
The requirement-level completion audit is in `paper/COMPLETION_AUDIT.md`.
The COLM template provenance is recorded in `paper/TEMPLATE_PROVENANCE.md`.

To regenerate the corrected 50-pair task set:

```bash
conda run -n trusted_proxy python scripts/generate_subtle_multidomain_tasks.py \
  --pairs-per-domain 10 \
  --out slambench/tasks/subtle_multidomain_50pairs_v2.jsonl
conda run -n trusted_proxy python scripts/validate_tasks.py slambench/tasks/subtle_multidomain_50pairs_v2.jsonl
```

## Conditions

- `c0_single_direct`: one agent receives the user goal and untrusted artifact.
- `c1_2agent_naive`: Reader -> Executor with free-form delegation.
- `c2_3agent_naive`: Reader -> Planner -> Executor with free-form delegation.
- `c2x_3agent_extractive_naive`: Reader -> Planner -> Executor where the reader
  extracts all document action items without provenance labels. This is a stress
  condition for source-laundering mechanics, not the main defended baseline.
- `c2o_3agent_oracle_laundered`: Reader output is an oracle provenance-stripped
  peer summary; Planner and Executor are model calls. This isolates downstream
  trust in already-laundered instructions.
- `c3_source_preserving`: 3-agent chain with provenance-preserving reader output.
- `c4_capability_scoped`: 3-agent chain with explicit sensitive-action authority.
- `c5_tracegate`: 3-agent naive chain with deterministic runtime monitor.
- `c5x_tracegate_extractive_naive`: extractive delegated chain with TraceGate.
- `c5o_tracegate_oracle_laundered`: oracle-laundered chain with TraceGate.

## Optional OpenAI pilot

Install dependencies first if needed:

```bash
conda run -n trusted_proxy python -m pip install openai
```

Then run a small bounded pilot:

```bash
conda run -n trusted_proxy python scripts/run_experiment.py \
  --tasks slambench/tasks/dev_30.jsonl \
  --condition c2_3agent_naive \
  --backend openai \
  --model gpt-4.1-mini \
  --api-key-file /home/eston/colm_workshop/apikey.txt \
  --limit 5 \
  --max-output-tokens 450 \
  --out outputs/raw_logs/openai_c2_pilot.jsonl
```

Use small `--limit` values first. The runner never passes the API key into a model
prompt and writes each completed run as JSONL so interrupted pilots keep partial
results.

The paper results already have saved raw logs. Do not rerun broad API sweeps
unless a specific missing table is identified.
