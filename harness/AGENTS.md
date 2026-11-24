# AGENTS.md

Done is a claim: a command exited 0 on this tree.

Codex concatenates this file with any `AGENTS.md` closer to the working directory. Closer files win because they are appended later. The combined text is capped by `project_doc_max_bytes`, 32 KiB unless someone raises it. Keep this file short so the cap does not cut off the rules.

## Working agreement

- Run `python3 .verify/verify_runner.py` before you claim a task is finished.
- Do not author a PASS line. The runner records exit codes.
- Stay inside the active brief's allowed files and respect its non-goals.
- Do not edit `.claude/`, `.verify/`, `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, or `.cursor/rules/`.
- Do not weaken an existing test, delete one, or skip it. New tests are welcome.
- `Verified-by: none` is a git trailer that needs an `Exemption-reason` a person can understand. It is not a phrase you drop into a command to skip the gate. CI re-runs the checks anyway.

## Code Review Rules

- Quote the command that ran and its exit code before you say the change is good.
- A green narrative with no command is not a review.
- Call out a diff that edits the harness, a test that already existed, or a file the brief does not list.

Claude Code reads `CLAUDE.md` and the hooks under `.claude/`. Cursor reads `.cursor/rules/verification.mdc`. This file is the Codex copy of the same agreement.
