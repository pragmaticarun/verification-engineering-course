# Quiz 3

### 1

Why is the done sentence copied into four files instead of one?

??? success "Answer"

    Claude reads `CLAUDE.md`, Codex reads `AGENTS.md`, Cursor reads the rule, and code review reads `REVIEW.md` from the protected base branch. One file leaves three tools on a different agreement.

### 2

What happens to a 40 KiB `AGENTS.md` in default Codex?

??? success "Answer"

    The combined project doc is capped at 32 KiB. The tail is not loaded. The auditor fails the file so you find out in CI rather than by watching a rule disappear.

### 3

A repository skill at `.claude/skills/verify/SKILL.md` does what to the bundled `/verify`?

??? success "Answer"

    It replaces the bundled skill. The template's skill runs the runner and forbids a handwritten PASS. A thinner skill would have taken over the built-in one and made it worse.

### 4

`permissions.deny` includes `Edit(.claude/**)`. Is that the lock on `main`?

??? success "Answer"

    No. It is a client control on Claude's Edit tool. A person, Codex, or a shell can still write the file. The runner also treats those paths as locked when it inspects the diff, and the ruleset plus CODEOWNERS is what can require a review. Module 4 separates those layers.

### 5

Why does `REVIEW.md` depend on branch protection?

??? success "Answer"

    Code Review reads it from the base branch. Without protection, the pull request can change the file that is supposed to judge the pull request. The template says so, and the ruleset file in `harness/.github/ruleset.json` is the shape you apply in the GitHub settings. Applying it is a repository setting, not a file commit.

### 6

The starter auditor only checks that `CLAUDE.md` exists. Name one failure it misses that the solution catches.

??? success "Answer"

    Any of: the shared sentence missing from `AGENTS.md`, the Cursor rule, or `REVIEW.md`; an `AGENTS.md` over 32 KiB; a deny list that does not mention `.verify` and `.claude`; settings that do not register Stop and PreToolUse.
