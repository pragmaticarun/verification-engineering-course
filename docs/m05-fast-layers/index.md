# 5. Fast layers

Coming soon.

The fast layer is the stack that finishes in under a minute: formatting, a linter, unit tests, and a golden file for a WAV header or a waveform PNG. It is the stack you can afford to run on every stop. Module 4's gate is only as good as the commands it runs, and a command that takes twenty minutes will get switched to observe.

The article's flaky-test rule belongs here. No sleeps, no skip, no retry-until-green. Delete the test and write down why. That policy is confirmed in the [verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/). Types, snapshots, and contract tests are the parts the article skips. [insta](https://insta.rs/docs/) and [cargo-nextest](https://nexte.st/) are the tools the later lab will pin. They are not in this milestone's CI.

On `pcmkit` the target is a `verify fast` that covers the Rust tests, the Python oracle, and the C++ consumer you can already run with `make check`, plus a golden header. The C ABI check stays in the fast layer because a signature change that only the Rust tests see will still link the consumer and then do the wrong thing.

!!! note "Codex and Cursor"

    A fast layer is a command, so it ports. Codex and Cursor will not grow a Stop hook. Put the command in `AGENTS.md` and the Cursor rule, and keep it in CI. The 32 KiB cap is a reason to name the command and not paste the whole style guide.

Back to the [syllabus](../syllabus.md).
