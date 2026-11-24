# 10. Agents verifying agents

Coming soon.

A second, more expensive reviewer is often worse than tuning the first. That is a reported result in the [verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/), and it matches the way a stack of comments feels like care while the bug ships. One reviewer, a rubric, observations before the score. The same note describes a rubric grader that added up to 10 points on structured file generation. The number is theirs. This course has not re-run the experiment.

The piece the article does not give you is a way to know the reviewer works. Known-bad incidents and known-clean merges, with a split between the set you tune on and the set you report. Precision and recall, on mocked reviews, with no API key. The note also says three bug-finders are replayed against known-incident pull requests, and that a rule is born from a miss: at least two pull requests, three agents try to disprove the rule, then a person opens the pull request that adds the check.

Claude Code's `/security-review` is a different tool with a documented entry point ([security](https://code.claude.com/docs/en/security)). It is not a substitute for a rubric you have scored.

!!! note "Codex and Cursor"

    Codex has a code-review mode and a "Code Review Rules" section in `AGENTS.md`. Cursor has Bugbot. Both can be the single reviewer. The rubric and the labelled incidents have to live in the repo either way, or you cannot compute precision. A review that only exists in a chat window is a claim.

Back to the [syllabus](../syllabus.md).
