# 9. Reward hacking and locks

Coming soon.

Module 4 shows that a local hook fails closed on a fixed corpus. This module is about the lock that still holds when the hook is not in the path. A person can commit. Codex can commit. A command can avoid the Bash tool. The article's own warning is the right one: a check the change can edit is a suggestion. The place the change cannot quietly edit is the server. Required checks, a ruleset, and code owners ([code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners), [code review at Anthropic](https://claude.dev/blog/solving-code-review-at-anthropic/)).

`harness/.github/ruleset.json` and `harness/.github/CODEOWNERS` are the template. Committing them does not enable them. GitHub applies a ruleset when you turn it on. The course root will say the same thing in its workflow: the jobs are necessary, and they are not sufficient until the branch requires them.

The corpus already includes test edits, skip markers, a special-cased test name, an equality override, and a call counter. Those are the ImpossibleBench shapes the excerpt supports ([paper](https://arxiv.org/abs/2510.20270)). This module adds a held-out suite the worktree does not contain, and a catch-rate line so a new cheat moves a number instead of a feeling. Two neighbouring papers, read from excerpts, are the reason to take the failure mode seriously and not a text to copy a method from: [monitoring reasoning models](https://arxiv.org/abs/2503.11926) and Anthropic's note on [reward hacking in production RL](https://www.anthropic.com/research/emergent-misalignment-reward-hacking).

!!! note "Codex and Cursor"

    Tell both tools not to edit the harness, and assume they might. The ruleset does not care which agent produced the diff. Cursor's Bugbot is a reviewer, not a lock ([docs](https://cursor.com/docs/bugbot)).

Back to the [syllabus](../syllabus.md).
