# Review rubric

Done is a claim: a command exited 0 on this tree.

Read this file from the base branch. A copy of it inside the pull request is the author talking to themselves.

Score only what you can point at.

1. **Command.** Which check ran, from the base `checks.json`, and what was its exit code?
2. **Scope.** Which files changed, and which of them are outside the brief?
3. **Tests.** Were any existing tests edited, deleted, or skipped? A new test is fine.
4. **Harness.** Did `.claude/`, `.verify/`, the instruction files, or CI change? That needs an owner.
5. **Not checked.** What did this run leave alone (a device, a long soak, a UI you could not open)?

Write those five observations first. The verdict is the last line, and it is one of `pass`, `fail`, or `needs-human`. A verdict with no observation above it scores zero.
