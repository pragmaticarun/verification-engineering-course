# Claude Code

Done is a claim: a command exited 0 on this tree.

## What to do before you stop

Run `python3 .verify/verify_runner.py`. Read the verdict it prints. That command executes the checks selected from the base branch. Do not write `VERDICT: PASS` into `evidence.md`. A line you typed is not a result, and touching the file to make it look new is not a result either.

If a brief is active, stay inside its allowed files. Non-goals in the brief are out of scope even when they seem helpful.

Adding a new test is part of the work. Changing or deleting a test that already exists on the base branch needs a person. Do not add `#[ignore]`, `pytest.skip`, or a branch that looks at the test's name.

## Hands off the harness

Do not edit `.claude/`, `.verify/`, `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, or `.cursor/rules/`. Do not set the gate mode to `off`. Do not remove a hook to get a commit through. A commit message that merely contains the letters `Verified-by: none` is not an exemption. An exemption is a trailer, with a reason a person can read, and CI still re-runs the checks.

## Where this file does not apply

Codex reads `AGENTS.md`, walking from the repository root toward the working directory, and stops after 32 KiB by default. Cursor reads `.cursor/rules/verification.mdc`. The done sentence above is copied in both, on purpose. Hooks in `.claude/settings.json` are Claude Code events. The check that actually blocks a merge is CI, which does not care which editor produced the diff.
