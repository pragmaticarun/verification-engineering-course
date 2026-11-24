# Verification Engineering for AI Coding Agents

A hands-on course for people who already ship C++, Rust, and Python and need a coding agent's "done" to be an exit code. The learner this milestone was written for is an Android and multimedia developer on Ubuntu. Claude Code is the tool the hooks attach to. Codex (`AGENTS.md`) and Cursor (project rules) get the same agreement, and CI is the lock.

Modules 1–8 are written. Modules 9–12 and the capstone are on the syllabus and marked coming soon.

| | |
| --- | --- |
| Read | `mkdocs.yml` builds the site with [Zensical](https://zensical.org/) 0.1.3 |
| Run | `pcmkit/`, a small WAV/PCM library, CLI, C ABI, and Python reference |
| Copy | `harness/`, instructions, permissions, hooks, and a ruleset template |
| Replay | `python3 tools/mockagent/replay.py` on recorded hook events |

No API key is required. CI does not call a model.

## Checks

```text
make check
```

That is the fast tier (format, clippy, tests, flaky-pattern scan, ruff, mypy, clang-tidy, the C++ consumer), then the oracle, a one-mutant smoke, the end-to-end golden, an ASan/UBSan build of the consumer, the normalize acceptance command, and the harness tests. Rust is pinned in `rust-toolchain.toml` (1.83.0). Python linters are pinned in `requirements-checks.txt`. A separate workflow runs one Miri test on `nightly-2026-11-23`. cargo-fuzz, Kani, and cargo-mutants are not installed.

```text
python3 -m venv .venv
.venv/bin/pip install -r requirements-docs.txt
.venv/bin/python -m zensical build --strict
```

Strict mode fails on a broken internal link. The Pages workflow runs the same build.

## Licences

Code is MIT (`LICENSE`). Prose is CC BY 4.0 (`LICENSE-CONTENT`).

## Pages

The workflow `.github/workflows/site.yml` uploads a Pages artifact and deploys with `actions/deploy-pages` on a push to `main`. A pull request only builds. GitHub will not publish until the repository's Pages source is **GitHub Actions** (Settings, Pages, Build and deployment, Source). The ruleset template in `harness/.github/ruleset.json` is also not enforced until you apply it. It expects status checks named `test` and `site`, which are the job names in the two workflows.

The design notes live in `planning/proposal.md`. The public lesson does not copy the source article. Citations are on the references page.
