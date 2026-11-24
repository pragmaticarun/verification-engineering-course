# Claim check

The article this course starts from is @0xarcos, "Verification Engineering: The $400K Skill of Running 30 Fable 5.2 Agents (Full Course)", posted 18 November 2026 ([status 2123038548580245659](https://x.com/0xarcos/status/2123038548580245659)). The ideas in the middle of it mostly track [How the Claude Code team thinks about verification](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) (Addy Osmani, 16 November 2026) and the Claude Code docs. The file-by-file harness is the author's reconstruction. It is not a dump of Anthropic's repository.

This page is a check of the article's claims against those primary sources. A confirmed claim can still be the wrong design. The gate modes are real, and the article's implementation of them is weaker than the one Anthropic describes. That distinction is the point of [module 4](m04-hooks-gates/index.md).

The Fable 5.2 announcement, "The proof passes. Of what?", ImpossibleBench, the Baker monitoring paper, and Anthropic's reward-hacking note have been read in full. The rows below stay inside what those pages say.

| Claim in the article | Status | What the primary source actually supports |
| --- | --- | --- |
| "Fable 5.2" names a real model | Confirmed | Anthropic announced Claude Fable 5.2 and Mythos 5.2 on 9 November 2026. [Announcement](https://www.anthropic.com/claude-fable-and-mythos-5-2). |
| "Last month I ran 30 Fable 5.2 agents", posted 18 November 2026 | Timeline does not fit | "Last month" is October. The public announcement is 9 November. The sentence only works if the author had access before the announcement, and the article does not say that. Treat the scene as an anecdote. |
| A salary above $400K for the skill, and $2,000 bootcamps | Unverifiable | No source is cited. This course does not repeat either figure as a fact. |
| About 90% of Claude Code is written and reviewed by Claude | Confirmed | Stated in the [verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) and the [code-review note](https://claude.dev/blog/solving-code-review-at-anthropic/). |
| A line attributed to Addy Osmani about the bottleneck moving to proving it works | Partial | The substance matches. The subtitle of [Agentic Verification](https://addyo.substack.com/p/agentic-verification) is "The bottleneck has moved from writing code to knowing it's correct". The article's wording was not found as a quotation. |
| Agents "basically didn't work before December and basically work since" | Confirmed as a February 2026 remark | Simon Willison recorded that Karpathy line in [February 2026](https://simonwillison.net/2026/feb/26/andrej-karpathy/). That remark does not contain the article's follow-on about tasks you can verify. |
| Agents work best where you can verify | A different primary source | The close line is Karpathy's [Verifiability](https://karpathy.bearblog.dev/verifiability/) (17 November 2025): "Software 2.0 easily automates what you can verify." |
| Karpathy asked for a proof next to the answer two years ago | Unverifiable | Not located in the sources fetched for this course. |
| `REVIEW.md` is read from the base branch, never from the pull request | Confirmed, with a condition | It is a Code Review feature, and it depends on branch protection. [Customize Code Review](https://code.claude.com/docs/en/code-review-customize). A file the pull request can replace is not a base-branch file. |
| A verify skill under `.claude/skills/`, used before commits | Confirmed, and the docs have moved | The verification note describes the practice. Current Claude Code also ships a bundled `/verify`, and a repo-root `.claude/skills/verify/SKILL.md` replaces it. [Skills](https://code.claude.com/docs/en/skills). The article does not mention the replacement. |
| A 39-item reliability checklist, selected by the diff, usually 3–10 checks | Confirmed | [Verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/). |
| Three failed rounds, then a person | Confirmed | Same note. Our gate uses that shape and writes an escalation file. The escalation is not a pass. |
| A second, more expensive reviewer is often worse than tuning the first | Confirmed | Same note. Module 10 (coming soon) is where we measure one reviewer instead of stacking two. |
| Models tend to leave a teammate's wrong work untouched | Unverifiable | Not in the sources fetched for this course. |
| A rubric grader added up to 10 points on structured file generation | Confirmed as reported | [Verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/). The note is the source of the number. We have not re-run the experiment. |
| A commit stamp can say "none" | Confirmed as a practice | Same note. The stamp's format is not published, so `Verified-by:` is the article's choice of spelling. We keep the spelling and we parse it as a trailer. |
| A commit gate with off, observe, and enforce, and a third try that is allowed | Partial | The modes, and "blocked twice, then allowed", are in the verification note. Anthropic's gate checks whether the session contained `/code-review` or `/verify`. The article's gate checks for a string in a file the agent writes. That is a weaker check, and [module 4](m04-hooks-gates/index.md) does not ship it. |
| A rule is born from a miss: at least two pull requests, three agents try to disprove it, then a human pull request | Confirmed | [Verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/). The same note says three bug-finders are replayed against known-incident pull requests. |
| Flaky tests: no skip, no sleeps, no retry-until-green; delete the test and document why | Confirmed | Same note. |
| Delete every check that has not fired in 60 days | Partial | The note says the list is tidied on a routine. Sixty days is the author's number. A check for a rare, expensive failure can be quiet for 60 days and still be the one you wanted. Module 12 (coming soon) weights that. |
| Boris Cherny formally verified the Agent SDK in Lean, in 16 pull requests | Confirmed, with the model and the object | His [account](https://www.linkedin.com/posts/bcherny_i-used-opus-55-to-formally-verify-the-claude-activity-7508309724598263808-TVJY) names Opus 5.5 and also TLA+. Barry's note [The proof passes. Of what?](https://stravica.ai/blog/the-proof-passes-of-what/) separates the code, the model, the property, and the requirement. A passing proof is about the model and the property. |
| A Stop hook that exits 2 keeps the session going, and PreToolUse can match Bash | Confirmed, and incomplete | [Hooks](https://code.claude.com/docs/en/hooks). The article omits `stop_hook_active` and the built-in cap of eight consecutive continuations. Our hooks exit 0 and return a JSON decision, which is the documented path, and they count the cap themselves. |
| Claude Code has a built-in security review | Confirmed | `/security-review` is documented in [Security](https://code.claude.com/docs/en/security). |
| Simon Willison describes agentic manual testing | Confirmed | [Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/). |
| Property tests kill no-op tests because the agent did not write the inputs | Partial | The agent usually writes the generator and the property too, so the blind spot can move into the test. Mutation testing is the direct check that a test can fail. [cargo-mutants](https://mutants.rs/), [mutmut](https://mutmut.readthedocs.io/en/latest/). |
| Locking the tests catches an agent that edits them | Partial | ImpossibleBench reports that read-only tests stop a direct edit and do not stop special-casing or operator overloading ([paper](https://arxiv.org/abs/2510.20270)). The same paper's taxonomy includes state recording. The tamper scan in this repo looks for those shapes. Held-out tests are a later module. |
| The three tests worth the investment are end-to-end, property, and differential | Confirmed as the recommendation | [Verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) and [Agentic Verification](https://addyo.substack.com/p/agentic-verification). `pcmkit` already has the differential half: a Python reference beside the Rust library. |

## What the article's own sketches get wrong

These are design defects in the reconstructed files, not claims about Anthropic. CI in this repository feeds each one a recorded session or a patch and expects a block, except the last, which is a property the lab replaces.

1. The gates look for `VERDICT: PASS` in a file the agent writes. Nothing runs a command.
2. Freshness is a timestamp. `touch` refreshes a stale pass.
3. The locked list omits `.claude/settings.json` and `.verify/gate.json`, so the agent can turn the gate off or unregister the hook.
4. The letters `Verified-by: none` anywhere in the shell command are treated as an exemption. No reason is required.
5. The prose says tests cannot be touched. The locked list does not include them. A blanket lock would also forbid new tests, so the policy has to split add from edit.
6. A base branch with no checks file triggers nothing. The script also reads the local `main`, which can be stale in a worktree.
7. A hook only sees the Bash tool inside Claude Code. A person, another tool, or a commit that does not go through that tool walks past it. The lock that holds is CI, a ruleset, and code owners.
8. The attempt counter is a file in the repo, shared by every session, and it ignores `stop_hook_active`.
9. A table promises a file list for scope creep. No file in the article implements it.
10. "The balance is never negative" is demonstrated with deposits only. The property cannot fail.

[Module 4's lab](m04-hooks-gates/lab.md) is the corrected gate. The corpus under `scenarios/` is the proof that the corrections fire.
