# Reproducing the Paper-Facing Results

This repository contains saved model logs and deterministic replay/scoring
scripts. Verifying the paper-facing claims does not require OpenAI API access.
The API backend is only needed for optional new model samples.

Run the commands below from the full repository root. The submission bundle is
an upload package for the paper PDF, supplement, LaTeX source, and metadata; it
does not include the saved raw logs or Python verification scripts.

## Environment

Use the project conda environment:

```bash
conda run -n trusted_proxy python -m compileall scripts src tests
conda run -n trusted_proxy python -m unittest discover -s tests
```

The paper build additionally expects `latexmk`, `pdflatex`, and `pdfinfo` on
the host path.

## Main Claim Verification

Validate the main paired task set:

```bash
conda run -n trusted_proxy python scripts/validate_tasks.py \
  slambench/tasks/subtle_multidomain_50pairs_v2.jsonl
```

Regenerate the deterministic TraceGate-pruned replay from saved raw logs:

```bash
conda run -n trusted_proxy python scripts/replay_tool_logs.py \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl \
  outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl \
  --out outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl
```

Regenerate the main scored table:

```bash
conda run -n trusted_proxy python scripts/analyze_results.py \
  outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl \
  --out-dir outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned \
  --tables-dir paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned
```

Expected headline values:

| Condition | BSR | IUSR | ASR | ATR | PDR | Blocks |
|---|---:|---:|---:|---:|---:|---:|
| `c0_single_direct` | 60% | 54% | 6% | 0 pp | 0% | 0 |
| `c2x_3agent_extractive_naive` | 70% | 50% | 22% | +16 pp | 77% | 0 |
| `c5x_tracegate_extractive_naive` | 66% | 64% | 0% | -6 pp | 69% | 11 |

## Follow-up Artifacts

The follow-up tables are already generated under `paper/tables/`. The
requirement-level evidence map is `paper/COMPLETION_AUDIT.md`, and the claim
boundary file is `paper/CLAIM_CHECKLIST.md`.

The fastest full consistency check is:

```bash
make -C paper
conda run -n trusted_proxy python scripts/make_artifact_manifest.py
conda run -n trusted_proxy python scripts/make_submission_bundle.py
conda run -n trusted_proxy python scripts/check_paper_artifacts.py
```

`scripts/check_paper_artifacts.py` checks required files, task/run counts,
main and follow-up metric invariants, mechanism audits, PDF page counts,
artifact hashes, submission-bundle freshness, zip payload freshness, and
release-facing redaction rules.

## Optional API Runs

Saved artifacts are the source of record for the paper. New API runs should be
small and should keep credentials outside the repository:

```bash
conda run -n trusted_proxy python scripts/run_experiment.py \
  --tasks slambench/tasks/dev_30.jsonl \
  --condition c2_3agent_naive \
  --backend openai \
  --model gpt-4.1-mini \
  --api-key-file "$OPENAI_API_KEY_FILE" \
  --limit 5 \
  --max-output-tokens 450 \
  --out outputs/raw_logs/openai_c2_pilot.jsonl
```

The runner writes completed runs incrementally as JSONL. No experiment contacts
real email, calendar, ticket, browser, or memory services; all tools are mocked.
