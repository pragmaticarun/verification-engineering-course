---
name: verify
description: Run the repository verification runner and treat its output as the verdict. Use before stopping or committing.
---

# Verify

A repository skill at this path replaces Claude Code's bundled `/verify`. Use this one. It runs the checks. It does not ask you to invent a pass.

## Steps

1. Run `python3 .verify/verify_runner.py` from the repository root.
2. If it exits non-zero, read the `PROBLEM:` lines and fix the code. Do not edit the harness to make the command quieter.
3. If it exits 0, you may summarize what the commands were. Quote the runner. Do not write your own `VERDICT: PASS`.
4. The runner copies `E2E:` and `NOT CHECKED:` lines from the stdout of the checks into `evidence.md`. Do not invent those lines, and do not turn a NOT CHECKED line into a pass. A listening note stays NOT CHECKED unless a person records it as an exemption trailer. The lines are notes. The verdict is the exit code.

## Do not

- Do not `touch` evidence to make it newer than the source.
- Do not set `.verify/gate.json` to `off`, and do not remove a hook from `.claude/settings.json`.
- Do not put `Verified-by: none` in a command string to slip past the commit hook.

Codex and Cursor do not load this skill. The same command is what `AGENTS.md` and `.cursor/rules/verification.mdc` tell those tools to run, and CI runs it again without a skill at all.
