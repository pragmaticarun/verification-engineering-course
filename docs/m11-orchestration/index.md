# 11. Orchestration

Coming soon.

"One worktree, one session" is the right constraint and, in the article, about one sentence. Several agents in one working tree will overwrite each other's evidence and each other's edits, and a green review of a commit that has since moved is a review of the old tree. The module is worktrees, a headless run, and a merge queue.

Claude Code documents [worktrees](https://code.claude.com/docs/en/worktrees), [headless runs](https://code.claude.com/docs/en/headless), [subagents](https://code.claude.com/docs/en/sub-agents), and [GitHub Actions](https://code.claude.com/docs/en/github-actions). Anthropic's notes on [long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) and the [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) are the design reading. GitHub's [merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) is the part that re-runs the checks on the commit you will actually merge. Codex cloud ([docs](https://developers.openai.com/codex/cloud)) and Cursor cloud agents ([docs](https://cursor.com/docs/cloud-agent)) are the other two ways a session stops being local. The gate still has to be the workflow.

The lab, when it lands, runs an orchestrator over four to eight mocked sessions. No live model. The sessions are the same kind of recording module 4 already replays, with a worktree each so their round counters and their evidence files do not collide.

!!! note "Codex and Cursor"

    A worktree is a git feature. The instruction file walk changes because Codex starts from the repo root and appends the nested file. Keep the nested file short. Cursor rules stay with the root unless you add a rule that is scoped. The merge queue does not know which product opened the pull request.

Back to the [syllabus](../syllabus.md).
