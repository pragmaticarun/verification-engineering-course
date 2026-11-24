# 6. Tests an agent cannot fool

Coming soon.

End-to-end, property, and differential tests are the three the [verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) says to invest in. `pcmkit` already has a differential check: `pcmkit/oracle/test_oracle.py` compares the CLI with a Python reference on the same samples. The module will add a round-trip property and a fuzz target for the WAV parser.

The correction this module exists to teach: a property test does not by itself kill a no-op test. The agent usually writes the generator. Mutation testing is the direct check that the test can fail ([cargo-mutants](https://mutants.rs/), [mutmut](https://mutmut.readthedocs.io/en/latest/)). Module 4's ledger lab is the small version. A balance property that only deposits cannot see a ledger that ignores withdrawals.

ImpossibleBench is the other half. A test directory the agent cannot edit still loses to a special case on the test's name, an equality that always returns true, or a counter that remembers it has been called ([ImpossibleBench](https://arxiv.org/abs/2510.20270), read from an excerpt). The tamper scan in `harness/.verify/tamper_scan.py` looks for those shapes on added lines. Held-out tests, which the agent does not see at all, are module 9.

Fuzzing references for the later lab: [cargo-fuzz](https://rust-fuzz.github.io/book/cargo-fuzz.html), [libFuzzer](https://llvm.org/docs/LibFuzzer.html), [proptest](https://proptest-rs.github.io/proptest/intro.html), [Hypothesis](https://hypothesis.readthedocs.io/en/latest/). None of them run in this milestone. Light CI stays the unit tests, the oracle, the consumer, and the corpus.

!!! note "Codex and Cursor"

    A property and an oracle are files in the repo. Both tools can be told to run them. Neither tool is the reason a mutated line fails. CI is.

Back to the [syllabus](../syllabus.md).
