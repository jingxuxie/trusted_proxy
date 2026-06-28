# Trusted by Proxy Artifact Manifest

This manifest records the paper-facing artifacts used for the current main claim.
Regenerate it with `conda run -n trusted_proxy python scripts/make_artifact_manifest.py`.

## Main Metrics

| Condition | Runs | BSR | IUSR | ASR | ATR | PDR | CNAS | Blocks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| c0_single_direct | 100 | 0.60 | 0.54 | 0.06 | 0.00 | 0.00 | 0.10 | 0 |
| c2x_3agent_extractive_naive | 100 | 0.70 | 0.50 | 0.22 | 0.16 | 0.77 | 0.31 | 0 |
| c5x_tracegate_extractive_naive | 100 | 0.66 | 0.64 | 0.00 | -0.06 | 0.69 | 0.00 | 11 |

## Files

| Path | Bytes | Records/Pages | SHA256 |
|---|---:|---:|---|
| `README.md` | 5691 |  | `0f2308537f8b8ae4fc95386b6b6d93923b2a9f73039e3f973e265de2d44214d6` |
| `trusted_by_proxy_research_plan.md` | 45848 |  | `340cb054605d9a8e50e6929c3720b0245ba66fe41b91ae5e2bffe4866b513d71` |
| `slambench/tasks/subtle_multidomain_50pairs_v2.jsonl` | 206200 | 100 | `01d0d04eba3f81dcea5ad24e6a3f913696fb889d504345061432715ce21381b6` |
| `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl` | 687426 | 100 | `563977b702a09d0324672511aecfe19a41c4ca4ba5a68af3a382c4eb0628705d` |
| `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl` | 1597138 | 100 | `804368812428973d7dc1bab2d7b6b4ee4224839034b1476f20dc61291a6b4fab` |
| `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl` | 1583252 | 100 | `6b867141016ccd22acb2216bf08b354aba102c01aa9e88e03c3fc038711f0e5d` |
| `outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl` | 3909960 | 300 | `b0d2b9759dee1f0477e28dffda52fec2bd90789b6ec2cd2e63750c9c35ff07da` |
| `outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/scored_runs.jsonl` | 129424 | 300 | `60e41d5484ad25f52806d4ff713fa28f82e075b4745c10d3a12e5e75b0056115` |
| `outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.jsonl` | 1063 | 3 | `39d3b1febed600125471297a919e45273b616f5c0a63fc23059ba153f87cdad1` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md` | 553 |  | `4bfbf9e30bf58ad92c66f73b2ba90afe708cc946e16dcf657d0c7a82c06ffd9b` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/payload_results.md` | 1082 |  | `684fd4ff45fd97e3680fbdf20830a1d4153b624b92e66e4ca654e8dcd12b2949` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/bootstrap_notes.md` | 234 |  | `61fe28a9ba94ddbf577ec15ba256835124798f2d0622850e9c1183111598104b` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/attack_reason_results.md` | 263 |  | `a1d6e986645930c20a266298190e4601928f45e0e9746d8b2e66bc6517520a89` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md` | 9110 |  | `0658c6163e695a7a4f1f9543d3582f6fbb5aff1f2a2ae90173d5dd0f935d0e5d` |
| `paper/main.tex` | 15706 |  | `e5e703bf0cd6eddb975fe72e78be663373c994866a23b0dc797f4fae57bd3b5a` |
| `paper/main.pdf` | 107666 | 5 | `f8ec39d4b090f24d13bdc95037e7688a138a3784fdde076fe0a0e8e4639eb2be` |
| `paper/supplement.tex` | 5124 |  | `6fde9c776b07b891f8fea53b3dfc5886bba89c6945f686345be3a177b8552059` |
| `paper/supplement.pdf` | 74670 | 2 | `0b0e270ef2270774a6809eedf00f65219cc544a8a5ffaa07ba5737f79b2546ea` |
| `paper/colm2026_conference.sty` | 7727 |  | `55962ae80c25a50335825c85d23eb5f1cd9015aa8e77f7af32b483b646c7483e` |
| `paper/colm2026_conference.bst` | 26973 |  | `2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5` |
| `paper/fancyhdr.sty` | 20521 |  | `b56ec4434b9f4607529a4b23dc68ad8d4b94f1f631c8cddaf7da78140d53a5ea` |
| `paper/natbib.sty` | 45154 |  | `88bc70c0e48461934cab5b2accef06b74a8b3ac45ad03ccd3f2a6b7e0d6d530d` |
| `paper/math_commands.tex` | 12284 |  | `90473c4d0542070db244cea73ef962d6cddc5b2a746757e6a40ddf5fdfb90ba9` |
| `paper/TEMPLATE_PROVENANCE.md` | 986 |  | `ff6b2ab990321aaf278e544cfe9edaf2701ca1c5e775d98ba6be4abad999d8c6` |
| `paper/refs.bib` | 1816 |  | `308af78f3116ed775bb451252f4cbb3119dad1617a8d4c17d55569f9ac3f456b` |
| `paper/RESULTS_SUMMARY.md` | 8929 |  | `4309710f149d4d2200553b98491a02177fb9f48f5322e81ef8919cd45d6cf946` |
| `paper/CLAIM_CHECKLIST.md` | 3809 |  | `e90e79e48291dfda19450a9c0e9fe828ceba248f71192d998e1843d767cf3a78` |
| `paper/SUBMISSION_CHECKLIST.md` | 5484 |  | `470d4b49096d1d5b5bd8dc1522e71fb6b8885a885cad52fe7667c20957a06245` |
| `paper/COMPLETION_AUDIT.md` | 4853 |  | `6fa0133a4029abe94ef6ba92bcacf25c61f328b8c677490042f16745d7a192a5` |
| `scripts/check_paper_artifacts.py` | 12159 |  | `401802391e8989495439bc94331a3ad84343d14b5546539aa5d38e9e731e2573` |
| `scripts/make_artifact_manifest.py` | 6073 |  | `3cd5ebdde7c1fecef2dd1135a051186aa4f256075c8f144fc6a85f9e9d60de83` |
| `scripts/make_submission_bundle.py` | 3749 |  | `b5ab90e9bef0c6e6ca46de069a2f094064c7b9aae22220c766c62b909783109b` |
| `src/scoring.py` | 10626 |  | `bf0bb2c94f209463f9953c3510b5dd550699d3e43c63d000c7077d86bb168af5` |
| `tests/test_scoring.py` | 3576 |  | `7ff3f2326ed3f34ea45960228c41ada62dcde6ce73d2c1b2f942f34931db5077` |
