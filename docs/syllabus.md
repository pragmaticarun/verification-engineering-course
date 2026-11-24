# Syllabus

Twelve modules, about four hours each, plus a capstone. Read for half an hour, then spend the rest in the lab and the project. At two modules a week this is six weeks and then the capstone. Go faster if the tests are already how you think.

The running example is `pcmkit`: a Rust WAV/PCM library, the `pcmx` CLI, a C ABI with a C++ consumer, and a Python reference. Each module adds a check or a rule to that tree. Claude Code is the tool with the richest hooks. Every module says what Codex (`AGENTS.md`) and Cursor (project rules) can and cannot see.

| Module | You come out able to | On `pcmkit` | Status |
| --- | --- | --- | --- |
| [1. Why verification](m01-why-verification/index.md) | Tell a claim from a result, and compute reads per ship | Replay ten mocked reviews and compare ticks with exit codes | Ready |
| [2. Defining done](m02-defining-done/index.md) | Write a brief an agent can fail | Brief and acceptance command for `pcmx gain --normalize` | Ready |
| [3. Instructions and permissions](m03-instructions-permissions/index.md) | Keep one agreement across Claude, Codex, and Cursor | Deny rules for the harness directories | Ready |
| [4. Hooks and gates](m04-hooks-gates/index.md) | Test a Stop hook and a commit hook on recorded events | Corrected gates, and the ten holes closed in CI | Ready |
| [5. Fast layers](m05-fast-layers/index.md) | Stack formatters, linters, unit tests, and golden files | `make fast`: rustfmt, clippy, goldens, ruff, mypy, clang-tidy, the C ABI | Ready |
| [6. Tests an agent can't fool](m06-cant-fool-tests/index.md) | Use properties, a differential oracle, a fuzz smoke, and a mutant | Fixed-seed properties, the Python oracle, one killed mutant | Ready |
| [7. Native and formal-lite](m07-native-formal/index.md) | Run sanitizers and a bounded check, and say what a proof is about | ASan/UBSan on the consumer, an exhaustive i16 grid, one Miri test, one Kani harness on `i8 / 16` | Ready |
| [8. Run it and prove it](m08-run-and-prove/index.md) | Generate evidence bound to a tree hash, including what you did not check | `pcmx` normalize plus a waveform golden, copied into the evidence file | Ready |
| [9. Reward hacking](m09-reward-hacking/index.md) | Catch test edits, special cases, skips, and a gate the agent switched off | A 30-scenario corpus, a tamper scan, and two held-out peak cases. The ruleset stays a template | Ready |
| [10. Agents verifying agents](m10-agents-verifying-agents/index.md) | Calibrate one rubric reviewer instead of stacking two | Mocked write-ups, precision 2/3 and recall 2/3 on the report split | Ready |
| [11. Orchestration](m11-orchestration/index.md) | Run several agents in worktrees through gates, CI, and a merge queue | Six git worktrees, stale reviews refused, budget 8. No live model | Ready |
| [12. Metrics](m12-metrics-ratchet/index.md) | Measure escapes, reads per ship, cost, and catch rate, and turn a miss into a check | A twelve-row report, and a pruner that keeps a quiet tamper check | Ready |
| [Capstone](capstone/index.md) | Publish a before/after on a real repo | Eight mocked pcmkit rows: tick-count ships 3 red checks, exit codes ship 0 | Ready |

Modules 9 and 4 overlap on purpose. Module 4 builds gates you can unit-test. Module 9 is where those gates meet branch protection, held-out tests, and the cases a local hook cannot see.
