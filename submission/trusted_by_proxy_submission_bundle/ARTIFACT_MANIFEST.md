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
| `README.md` | 9246 |  | `b70c73178839746eb21851d6fa0c14d0e5d313615e25d2b8ebac471f9bf00b67` |
| `REPRODUCE_MAIN_RESULTS.md` | 3498 |  | `94debaa74c87f197b336819316ae63f5d352186c79dc984e1968e77150ed47cd` |
| `trusted_by_proxy_research_plan.md` | 45848 |  | `340cb054605d9a8e50e6929c3720b0245ba66fe41b91ae5e2bffe4866b513d71` |
| `followup_experiments_plan.md` | 4243 |  | `5dfe699a4c4d0232f167add9a247b0d8252e192faa6998288440e7bcd5ac645b` |
| `slambench/tasks/dev_30.jsonl` | 117600 | 60 | `078514c8f505e54637f32061d92118ceb86822de99f924619bf66972bb1efae0` |
| `slambench/tasks/subtle_multidomain_50pairs_v2.jsonl` | 206200 | 100 | `01d0d04eba3f81dcea5ad24e6a3f913696fb889d504345061432715ce21381b6` |
| `slambench/tasks/subtle_multidomain_25pairs_v2.jsonl` | 103076 | 50 | `7e2173da3a19edc23dad01138e1b25e9b4dc089001b9191085b0ccb7442f3865` |
| `slambench/tasks/subtle_multidomain_5pairs_v2.jsonl` | 17665 | 10 | `a04bb4bff334fe829da6a7a4d92cca4b9f86c9999c8ef289a316b048c2f80798` |
| `slambench/tasks/subtle_multidomain_repeatability_6inj_v2.jsonl` | 13517 | 6 | `da00da103e7e3dd1dfdfd97acd121821443d2e365bbae406fdd2683f2a5461c0` |
| `slambench/tasks/subtle_multidomain_hard6pairs_v2.jsonl` | 25922 | 12 | `698092ea65d1f1bf42ebbbb25b2557305f54a1be9388cc6bb1bc40b31244bc1f` |
| `slambench/tasks/nonemail_side_effects_3pairs_v1.jsonl` | 12192 | 6 | `b2980e9faee6b73d32d126eeec4dde8eeb63dc2210be4bc816acca255c5c1c1f` |
| `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c0.jsonl` | 687426 | 100 | `563977b702a09d0324672511aecfe19a41c4ca4ba5a68af3a382c4eb0628705d` |
| `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c2x.jsonl` | 1597138 | 100 | `804368812428973d7dc1bab2d7b6b4ee4224839034b1476f20dc61291a6b4fab` |
| `outputs/raw_logs/openai_schema_prompt_50pairs_gpt54nano_c5x.jsonl` | 1583252 | 100 | `6b867141016ccd22acb2216bf08b354aba102c01aa9e88e03c3fc038711f0e5d` |
| `outputs/replayed_logs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned.jsonl` | 3909960 | 300 | `b0d2b9759dee1f0477e28dffda52fec2bd90789b6ec2cd2e63750c9c35ff07da` |
| `outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/scored_runs.jsonl` | 129424 | 300 | `60e41d5484ad25f52806d4ff713fa28f82e075b4745c10d3a12e5e75b0056115` |
| `outputs/scored_runs/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.jsonl` | 1063 | 3 | `39d3b1febed600125471297a919e45273b616f5c0a63fc23059ba153f87cdad1` |
| `outputs/raw_logs/followup_gpt55_25pairs_1200_c0.jsonl` | 360282 | 50 | `d587957c82379a856ad060e473cdadc4534982ca488c4d3ff756954746c6d702` |
| `outputs/raw_logs/followup_gpt55_25pairs_1200_c2x.jsonl` | 875606 | 50 | `a7c5a09c80d22a965f1d2f9a7bf17f4f277a60819ce87422bb95ca429deafe38` |
| `outputs/raw_logs/followup_gpt55_25pairs_1200_c5x.jsonl` | 856080 | 50 | `4997035b3bba05d00410256e0204697640ba119ad799ab78b4f2d195a58ef9c1` |
| `outputs/scored_runs/followup_gpt55_25pairs_1200_core/scored_runs.jsonl` | 63717 | 150 | `6cac8d67ba7cc560bfa4d1b96bddcc882054d70a95f7a1026bb9e467018a89fe` |
| `outputs/scored_runs/followup_gpt55_25pairs_1200_core/main_results.jsonl` | 977 | 3 | `f1bc8f4f2646298d474040e37883be3118cc5fd8749639ba12fe4e8d0b2030f5` |
| `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c0.jsonl` | 344995 | 50 | `a634298e09028b7dd315f867276b820afc57043687d8d63db36d30ca98f7fcd3` |
| `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c1.jsonl` | 504446 | 50 | `fb58a2341d53ee70e44b544e9a2b6070c037f339878308ff3ed58fdb7257f962` |
| `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2.jsonl` | 896909 | 50 | `f6ad2cdb3476781ae81f426f9692d622d88bd0e759e4d5f2ebe4bf9318d44fe5` |
| `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2x.jsonl` | 956988 | 50 | `2c5b07538756bb81cca67f517e55dbff1b26f5414714cf7d182a58c64d960d3f` |
| `outputs/raw_logs/followup_gpt54nano_25pairs_1200_topology_c2o.jsonl` | 743588 | 50 | `a097fa189dcd06845e2c738c57d61619add8762cc4471406d35e5a1d13360ce2` |
| `outputs/scored_runs/followup_gpt54nano_25pairs_1200_topology/scored_runs.jsonl` | 105522 | 250 | `4837ef4b0c2da261e8f1b5a4043bb6a85b6f48267abbab65ed3158b25f844673` |
| `outputs/scored_runs/followup_gpt54nano_25pairs_1200_topology/main_results.jsonl` | 1814 | 5 | `60b6d5be639c40003d9c388f5d9de300f2b6441ee63339ea1e65ed7326526cad` |
| `outputs/analysis/followup_gpt54nano_25pairs_1200_topology_mechanism/provenance_flow_runs.jsonl` | 63769 | 125 | `edfa0def8f3768b923ff4fe22fb92c342ce1e115bbbe988abd6e2391ae45d8ca` |
| `outputs/analysis/followup_gpt54nano_25pairs_1200_topology_mechanism/provenance_flow_summary.jsonl` | 1127 | 5 | `c72c58828c9800f289e62aaac3ca6ba022900785222152068a3a5a2d600ef046` |
| `outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c3.jsonl` | 1037086 | 50 | `81c876d160a0cb9836f34b24c9caedae8450f48ccb6e97a2eeb94a9fc8aa153b` |
| `outputs/raw_logs/followup_gpt54nano_25pairs_1200_defense_c4.jsonl` | 919816 | 50 | `e6c4acfc07db658e2a4b83c19a6297ee9481f3e00469789cc3c4e37a75034870` |
| `outputs/replayed_logs/followup_gpt54nano_25pairs_1200_defense_c5x_replay_from_c2x.jsonl` | 972696 | 50 | `7521a97c7255609cad98c39d34808e440a65eeca145f07dad84634c0b07e5566` |
| `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense/scored_runs.jsonl` | 109354 | 250 | `e221078986c5691bec8ea32ef8ba4d7e939088039d000602312c974aa86af1ab` |
| `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense/main_results.jsonl` | 1737 | 5 | `824138290f6d9a5f376910a4bd7dd80ffee89baf25a41247207ab94be794992c` |
| `outputs/analysis/followup_gpt54nano_25pairs_1200_defense_mechanism/provenance_flow_runs.jsonl` | 64113 | 125 | `9662c0dfc35e70cacbaf8f17ad02109202e23b7f7d73aa7ea048d51ff52248bf` |
| `outputs/analysis/followup_gpt54nano_25pairs_1200_defense_mechanism/provenance_flow_summary.jsonl` | 1145 | 5 | `27ad8e916fc074ea33a38bf997bfa727889ef0ac0667fff89bd2aaf6f7485eb8` |
| `outputs/replayed_logs/followup_gpt54nano_25pairs_1200_guard_c6_from_c2x.jsonl` | 1252036 | 50 | `e9d1b135843bf3898956eba2a99c78157566f7c8c52401fe411e5e6c8ecbe63e` |
| `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_guard/scored_runs.jsonl` | 131548 | 300 | `bf2e18617e7b66f9ca4ede3fdb6222baaccb9b63739ae5a0218c6365e6605b9a` |
| `outputs/scored_runs/followup_gpt54nano_25pairs_1200_defense_guard/main_results.jsonl` | 2075 | 6 | `4c12e64cbfde53c17e2a552291761bf8694a5f77dbc45ce6de21b9a503e1477f` |
| `outputs/raw_logs/followup_gpt54nano_repeatability_6inj_c0_3runs.jsonl` | 129053 | 18 | `08452d69dd478c98edcac1c67b0f197202b79e1abeb3dbc8de395f39433f9a8f` |
| `outputs/raw_logs/followup_gpt54nano_repeatability_6inj_c2x_3runs.jsonl` | 341961 | 18 | `4870dfab0798158d9759f14eee22df96ad42ebbcb030fdf54b8b1675e53a8a0a` |
| `outputs/replayed_logs/followup_gpt54nano_repeatability_6inj_c5x_replay_from_c2x_3runs.jsonl` | 348458 | 18 | `3d16705c46daed6f9dfc7f0ab219342a70097f3bfd953234652aa7ced06fd907` |
| `outputs/scored_runs/followup_gpt54nano_repeatability_6inj_3runs/scored_runs.jsonl` | 24822 | 54 | `7512b54fa9581f61c2d7d6ca9a92f36808c8322e9ec785a2b5bd05a452517165` |
| `outputs/scored_runs/followup_gpt54nano_repeatability_6inj_3runs/main_results.jsonl` | 1068 | 3 | `d401162afdc41a2795b9525d42a41d5d5ed50278b9780158d9466eef376df6c7` |
| `outputs/raw_logs/followup_gpt54nano_nonemail_3pairs_c0.jsonl` | 41122 | 6 | `84ac83f82af60998222dc6ca61dbb54a97dc14a5b40bf8bff7a3f45306051b09` |
| `outputs/raw_logs/followup_gpt54nano_nonemail_3pairs_c2x.jsonl` | 117640 | 6 | `538629dc222e3a7c3aa4353c971f83e2e81090a72e3333cd9b33411f5dd8c815` |
| `outputs/replayed_logs/followup_gpt54nano_nonemail_3pairs_c5x_replay_from_c2x.jsonl` | 119294 | 6 | `39f00cd0a009d25bc2ed13f49e903086b3df158e10f0953b01507c58195a823e` |
| `outputs/scored_runs/followup_gpt54nano_nonemail_3pairs/scored_runs.jsonl` | 8136 | 18 | `718d4dda2adc13da38536edd092e25b8c2589f7a6fbde070a0da79ea961f7da6` |
| `outputs/scored_runs/followup_gpt54nano_nonemail_3pairs/main_results.jsonl` | 1155 | 3 | `3aeb9fc51658cc8798d5cb98a0a2443fea76d76fb838c57702d9e0f8e50004e2` |
| `outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x.jsonl` | 216728 | 12 | `3ac214693c77485b53e57ec110d61e67d16f9bf4c334e60e59f603dfc5c27202` |
| `outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x_with_parser_error.jsonl` | 210712 | 12 | `34feae99cea42cdb81340d826b754c7f9fa8d536b6a24e5108133dc13608a9b1` |
| `outputs/raw_logs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x_repair_research_subtle_002.jsonl` | 23745 | 1 | `b4df4654bad3d8cd1ee8f7a9e692b8c420cf8418cd0c8d1b7f143be282994869` |
| `outputs/scored_runs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/scored_runs.jsonl` | 6089 | 12 | `ff3f0034e8b13688f8e28f62a98a88a0d28c30e79479e9682875292be0de59fe` |
| `outputs/scored_runs/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/main_results.jsonl` | 441 | 1 | `074dd04731f163898b350d10882112c059bf08efb726285de7483ffbea141b6e` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/main_results.md` | 553 |  | `4bfbf9e30bf58ad92c66f73b2ba90afe708cc946e16dcf657d0c7a82c06ffd9b` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/payload_results.md` | 1082 |  | `684fd4ff45fd97e3680fbdf20830a1d4153b624b92e66e4ca654e8dcd12b2949` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/bootstrap_notes.md` | 234 |  | `61fe28a9ba94ddbf577ec15ba256835124798f2d0622850e9c1183111598104b` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/attack_reason_results.md` | 263 |  | `a1d6e986645930c20a266298190e4601928f45e0e9746d8b2e66bc6517520a89` |
| `paper/tables/openai_schema_prompt_50pairs_gpt54nano_tracegate_pruned/trace_examples.md` | 9110 |  | `0658c6163e695a7a4f1f9543d3582f6fbb5aff1f2a2ae90173d5dd0f935d0e5d` |
| `paper/tables/followup_gpt55_25pairs_1200_core/RESULT_SUMMARY.md` | 2587 |  | `ea47d4be1a2126aee651a399d917de0da186d3be9ec057a5dc85a803afcacd53` |
| `paper/tables/followup_gpt55_25pairs_1200_core/main_results.md` | 548 |  | `627f749ddd42a76742b7d8b9677c18d29c411f945fa5593921117385d68b9e55` |
| `paper/tables/followup_gpt54nano_25pairs_1200_topology/RESULT_SUMMARY.md` | 3319 |  | `20d61d93a0d104687ada5c42f040d9363e9bfffa30a82ff57b0511234b14e450` |
| `paper/tables/followup_gpt54nano_25pairs_1200_topology/main_results.md` | 776 |  | `9fa9d7326207976a1613a526d17296890b5863dceb7904d55965e00b4e056e3b` |
| `paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism/provenance_flow_summary.md` | 581 |  | `25a04ee3e417d863359c6748b41e66f001f836b3fc298afa29cf5a9e5257d584` |
| `paper/tables/followup_gpt54nano_25pairs_1200_topology_mechanism/differential_attack_cases.md` | 971 |  | `383a2fe3987cee8ee6b1657d964eb2d4fac5753f857e538e1f3564176c447e66` |
| `paper/tables/followup_gpt54nano_25pairs_1200_defense/RESULT_SUMMARY.md` | 3488 |  | `ad9e74b1a5d8bb3266867da01e5f18d46bbf19601e458531ecf01e84527ad048` |
| `paper/tables/followup_gpt54nano_25pairs_1200_defense/main_results.md` | 789 |  | `b90e4b9cce5c9c16ebf660185b31388db1da11b36b3b44a7dbc66de3c2827ffa` |
| `paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism/provenance_flow_summary.md` | 597 |  | `65759fc9b15ba8e09433f588ef846634cbd26bd8f995a6e3704cfa6f26d856f3` |
| `paper/tables/followup_gpt54nano_25pairs_1200_defense_mechanism/differential_attack_cases.md` | 971 |  | `383a2fe3987cee8ee6b1657d964eb2d4fac5753f857e538e1f3564176c447e66` |
| `paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/RESULT_SUMMARY.md` | 2179 |  | `ca42a3bf4aab032d6cd9618dc0ba3799e239978f50540eb08718711ac31bae5d` |
| `paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/main_results.md` | 917 |  | `c6f659c0210b6c714abe41d266d18765fa31b09ab46475672fb2a0a0fecada35` |
| `paper/tables/followup_gpt54nano_25pairs_1200_defense_guard/bootstrap_notes.md` | 565 |  | `1174a9522046e96c009bb5f44c2645bb8acad02f629d1eb18b2e34b1430afc6b` |
| `paper/tables/followup_gpt54nano_repeatability_6inj_3runs/RESULT_SUMMARY.md` | 3087 |  | `ef488ce77b7d094b1aaa5a03f942612dab221494bcaa38ef1192fbd9ef482735` |
| `paper/tables/followup_gpt54nano_repeatability_6inj_3runs/main_results.md` | 560 |  | `7fac81c232ce7da6fa38f6a0058c17f8f7416eab06b58d8dd881584b1c852562` |
| `paper/tables/followup_gpt54nano_nonemail_3pairs/RESULT_SUMMARY.md` | 2764 |  | `e69294673f64ed0a1cfabe5ddf72840e9f9880c213daac73b79721d524d55bfe` |
| `paper/tables/followup_gpt54nano_nonemail_3pairs/main_results.md` | 542 |  | `8315b914000d00883783044793c83d6eb7eb7e5c09f289835746b0a95a7efb79` |
| `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/RESULT_SUMMARY.md` | 3159 |  | `e512cf808a64363719620abafcb8b0f173d27580b886adf3e08134e049570190` |
| `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/main_results.md` | 305 |  | `4e45236281a854c08aed351633bb8a0eb993757bc4ad3d3dabe1d1380d666118` |
| `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/payload_results.md` | 361 |  | `e0e3ec0f7cbf9071b985dbcacbc3654763fbddaaa3a4bea9076ae2cfcf8570b9` |
| `paper/tables/followup_hetero_hard6pairs_readerplanner54nano_executor55_c2x/hard_slice_comparison.md` | 828 |  | `1becc6197af82505166b6a67506a59583286e6a5c874af7806985f15bb28c05b` |
| `paper/main.tex` | 23032 |  | `72736b524565a66f7e97a469d7aaf561b1bd00b063bc23f1a846eae7ff134c3d` |
| `paper/Makefile` | 353 |  | `741442d61935f7efa8508a7b7201109cf486391f8e6bc8fb4a00599ec9393c78` |
| `paper/main.pdf` | 132429 | 7 | `c96e3ff934dec2d8a7703109ec00bbf05f34cf4fe7a03ada10ca1fc53fd325a3` |
| `paper/supplement.tex` | 5124 |  | `6fde9c776b07b891f8fea53b3dfc5886bba89c6945f686345be3a177b8552059` |
| `paper/supplement.pdf` | 74670 | 2 | `0b0e270ef2270774a6809eedf00f65219cc544a8a5ffaa07ba5737f79b2546ea` |
| `paper/colm2026_conference.sty` | 7727 |  | `55962ae80c25a50335825c85d23eb5f1cd9015aa8e77f7af32b483b646c7483e` |
| `paper/colm2026_conference.bst` | 26973 |  | `2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5` |
| `paper/fancyhdr.sty` | 20521 |  | `b56ec4434b9f4607529a4b23dc68ad8d4b94f1f631c8cddaf7da78140d53a5ea` |
| `paper/natbib.sty` | 45154 |  | `88bc70c0e48461934cab5b2accef06b74a8b3ac45ad03ccd3f2a6b7e0d6d530d` |
| `paper/math_commands.tex` | 12284 |  | `90473c4d0542070db244cea73ef962d6cddc5b2a746757e6a40ddf5fdfb90ba9` |
| `paper/TEMPLATE_PROVENANCE.md` | 1075 |  | `43a163374601d7746935b55979bf83aca55b7108b60d034f1bb9ac0cd9ce4fa3` |
| `paper/refs.bib` | 4897 |  | `5082e269c1325d836cfd67f603d95bc01c2fc0d74cccca4f56509a6de0ec1989` |
| `paper/RESULTS_SUMMARY.md` | 10722 |  | `f257544bbdb1b684d609f71196f8d3b6d072669b29e6f10b7cdf914d5d75446a` |
| `paper/CLAIM_CHECKLIST.md` | 6995 |  | `ba129d78f01b91832bccc66ab3ba18e7cc02ab12662f769cc9706c00313d8cf8` |
| `paper/SUBMISSION_CHECKLIST.md` | 6813 |  | `05f60f71853a8b2439d98a687346720183a5a2e4710ea8a6a51a3fb12e49d3c9` |
| `paper/COMPLETION_AUDIT.md` | 11233 |  | `caa1b2b14f87d08db1358fe89b8294e17716ee6cc947f6bf5289db2a26330d0f` |
| `scripts/check_paper_artifacts.py` | 41889 |  | `1f12aa901074f79b412d16ca834255744ac37234309b653d8092fff655181f20` |
| `scripts/analyze_results.py` | 9498 |  | `db25f55b6dd633926a74a107b0977a49877b125f837fa67c9d36df1073b0a9c8` |
| `scripts/analyze_provenance_flow.py` | 10419 |  | `3ba0ad3873e55edb1881f9541277a7174a819164d188084804fb3e046fd8692e` |
| `scripts/validate_tasks.py` | 1946 |  | `902027e18ece5b8e7098ee1babd20f08a2fc1c19bfe26a6d3b5c66a6cb9a26b4` |
| `scripts/generate_subtle_multidomain_tasks.py` | 6066 |  | `8a1c27630ebf916a84f0be16732228de4dd4ea354139196d828f589e01f2619f` |
| `scripts/generate_nonemail_side_effect_tasks.py` | 4685 |  | `26e77c54e33126b23763429b5acfd37af00f7124438b626f23006ded476973aa` |
| `scripts/make_artifact_manifest.py` | 12121 |  | `e13024d79c17cd5ef27e10c741a5d65857155de4261eaeaeff17a9a7f6e6f081` |
| `scripts/make_submission_bundle.py` | 4704 |  | `2bc18e731a3d6cd4341e3ec74216cc017aec2547482d2b219700f98a164a2988` |
| `scripts/make_paired_subset.py` | 3132 |  | `3cc797f9e6f4681fb240d600cf12e6b6760376e8afad68f2bd50a5c4e56ddbe2` |
| `scripts/replay_tool_logs.py` | 2177 |  | `49666677cf85a9c7ab0c0bb645d2db6f0e016e4cb43f429bf150a9e542435175` |
| `scripts/replay_with_llm_guard.py` | 6217 |  | `14bb574b5eb612ded4587fda85e0905c1ec63109be3454ab09169a4df06bb586` |
| `scripts/run_heterogeneous_experiment.py` | 4561 |  | `e7ec2a4ffb9bd8274a672102dc63e15e87695f5ef2eb119d93d45f8f17e7810d` |
| `scripts/run_experiment.py` | 3272 |  | `0651c061ca9d4c52e58a11e1c086d2f3859c9a6fa3b6934bc69f02b18b2ef1b7` |
| `scripts/summarize_openai_usage.py` | 4492 |  | `b675cf6f5aed793b1b26ee29dfdf1cfb37aa2af07907cc1026ee5412db82b96b` |
| `src/scoring.py` | 11200 |  | `fe860ecb2228d355bb49d34d113084eeb1dbee2a15ed7f0fbbdac9580f0feb69` |
| `src/tools.py` | 10329 |  | `e4d0ac46bcfbbf9b8de9ff678ec187357c5d327e3064c8bd7ccc69b728bf91c4` |
| `tests/test_scoring.py` | 6004 |  | `0a2e4a755a9da91516a70f5e5d4d5c4efd07b1111dc136d57539726fa5b1ab4e` |
