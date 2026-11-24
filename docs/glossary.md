# Glossary

**Acceptance command.** A command named in a brief before the code exists. Done means that command exited with the status the brief names.

**Allowed files.** The paths a brief says the change may touch. A diff outside that list is scope creep, even when the new code is good.

**Base ref.** The branch the pull request is merging into, usually `origin/main`. Checks, the gate mode, and the brief are read from that ref. The copy in the worktree is what the agent can edit.

**Catch rate.** The fraction of a fixed cheat corpus the harness rejects. A high rate on a toy corpus is a start, not a proof.

**Done.** A claim that some command exited 0 on this tree. The sentence is copied into `CLAUDE.md`, `AGENTS.md`, and the Cursor rule so the three tools share it.

**Evidence.** A JSON record the runner writes after it executes commands: exit codes, hashes of the output, a hash of the tree, tool versions. The Markdown beside it is for people. Editing the Markdown does not change the record.

**Exemption.** A git trailer `Verified-by: none` together with a substantive `Exemption-reason`. It is a recorded decision that a person skipped the local gate. CI still runs. A mention of the phrase in the middle of a command is not an exemption.

**Fail closed.** If the base ref has no checks file, or the hook cannot parse its input, the gate blocks. Silence is not a pass.

**Gate mode.** `off` does nothing. `observe` logs the decision and allows the action. `enforce` blocks. The mode that counts is the one on the base ref.

**Held-out tests.** Tests CI runs that the agent does not see in the worktree. They are a later module. This milestone's corpus is visible, and it is still enough to show a gate failing open.

**Locked path.** A file the change is not allowed to edit: hooks, settings, the checks file, the gate file, the instruction files. The minimum list lives in the runner, so deleting it from `checks.json` does not unlock it.

**Reads per ship.** Of the changes you actually shipped, the fraction where a person opened the diff. The goal is a small number because the checks were enough. It is not a goal of zero on payments, auth, or deletion.

**Round.** One time the stop gate refused to let the session end. After two refusals the third stop is allowed to end, and the runner writes `NEEDS-HUMAN.md`. That is an escalation, not a pass. Claude Code also stops honouring blocks after eight continuations in a row with no tool call. The gate honours that cap itself.

**Tree hash.** A hash of the worktree contents, excluding the evidence files the runner is about to write. A PASS bound to yesterday's hash does not cover today's edit. Updating a timestamp does not update the hash.

**Trailer.** A `Key: value` line in the trailer block of a commit message, or a `git commit --trailer` argument. The gates parse trailers. They do not search the raw command for a magic substring.
