# Setup

You need Ubuntu (or anything else that runs the same three tools), Python 3.12, Rust 1.83.0, and a C++ compiler. You do not need an Anthropic key, an OpenAI key, or a Cursor token. CI replays recorded hook events and runs `pcmkit` locally.

```text
python3 --version
rustc --version
g++ --version
```

The Rust toolchain is pinned in `rust-toolchain.toml`. The docs builder is pinned in `requirements-docs.txt` (`zensical==0.1.3`).

## Checks

```text
make check
```

That formats and clippy-checks `pcmkit`, runs its tests, runs the Python oracle, builds the C++ consumer, runs the normalize acceptance command, and runs the harness unit tests. The harness tests include the cheat corpus. The first run compiles Rust. Later runs are quick. Cargo's target directory is `target/` at the repo root so the crates share one build.

`make doctor` prints versions and a disk summary. `make fast` is the tier module 5 describes: format, clippy, tests, the flaky-pattern scan, ruff, mypy, clang-tidy, and the C++ consumer. Install the pinned Python tools first (`ruff==0.17.6` and `mypy==2.4.1` in `requirements-checks.txt`) and have `clang-tidy` on `PATH`. The default Ubuntu package is clang-tidy 18, which is what the lesson was run against.

`make check` adds the oracle, the one-mutant smoke, the end-to-end golden, the sanitizer build of the consumer, the acceptance command, and the harness tests.

A separate workflow, job `heavy`, is not one of the two status checks the ruleset template names. It still fails the pull request when it fails. On `nightly-2026-11-23` it runs one Miri test (`miri_gain_of_zero_is_finite`), then `bash tools/heavy/mutants.sh` (cargo-mutants 26.0.0, file `clamp.rs`, 9 caught, 2 equivalent misses), then `bash tools/heavy/fuzz.sh` (cargo-fuzz 0.13.2, target `wav_parser`, 15 seconds), then `bash tools/heavy/kani.sh` (`kani-verifier` 0.68.0, harness `clamp_unit_holds_an_i8_grid`). The stable toolchain does not ship Miri. cargo-fuzz 0.13.2 does not build on 1.83.0. Kani's bundle installs its own nightly, `nightly-2026-08-21`. mutmut, insta, nextest, proptest, Hypothesis, and Criterion are cited and not installed.

## The site

```text
python3 -m venv .venv
.venv/bin/pip install -r requirements-docs.txt
.venv/bin/zensical build --strict
```

Strict mode fails the build on a broken internal link. The published site is the same command in GitHub Actions, then `actions/deploy-pages` on a push to `main`. A pull request only builds. Publishing needs the repository setting Pages, Source, GitHub Actions. The workflow cannot switch that setting on for you. The ruleset template under `harness/.github/ruleset.json` is the same kind of thing: it is in the repo, and GitHub enforces it only after you apply it. It expects the job names `test` and `site`.

## No live model

`tools/mockagent/replay.py` builds a throwaway git repository, feeds the hook scripts the JSON Claude Code would write to stdin, and checks the decision. `LIVE=1` is reserved for a later, optional, local experiment against a real agent. It is not implemented in this milestone and CI never sets it.

## Copying the harness

`harness/` is a project root you can copy into another repository: instructions, settings, hooks, the runner, and a ruleset template. In this course repo it stays in `harness/` so the lessons and the tests share one copy. The checks file's commands assume the course layout (`pcmkit/`, `briefs/`, `tests/`).
