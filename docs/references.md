# References

Links are to the publisher. The course text is original. The Fable 5.2 announcement, "The proof passes. Of what?", ImpossibleBench, the Baker monitoring paper, and Anthropic's reward-hacking note were read in full before modules 5–8 quoted them. The course paraphrases those pages and cites them. It does not paste them.

## The article

- @0xarcos, "Verification Engineering: The $400K Skill of Running 30 Fable 5.2 Agents (Full Course)", 18 November 2026. [Post](https://x.com/0xarcos/status/2123038548580245659).

## Anthropic and Claude Code

- Introducing Claude Fable 5.2 and Mythos 5.2, 9 November 2026. [Announcement](https://www.anthropic.com/claude-fable-and-mythos-5-2). Excerpt at design time.
- Addy Osmani, "How the Claude Code team thinks about verification", 16 November 2026. [claude.dev](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/).
- "How the Claude Code team does code review", 15 October 2026. [claude.dev](https://claude.dev/blog/solving-code-review-at-anthropic/). The review-volume and revert-share figures used in module 1 come from this note.
- Customize Code Review, including `REVIEW.md` and branch protection. [Docs](https://code.claude.com/docs/en/code-review-customize). [Code Review](https://code.claude.com/docs/en/code-review).
- Skills, including the bundled `/verify` and how a project skill replaces it. [Docs](https://code.claude.com/docs/en/skills).
- Hooks. [Docs](https://code.claude.com/docs/en/hooks).
- Security, including `/security-review`. [Docs](https://code.claude.com/docs/en/security).
- Permissions. [Docs](https://code.claude.com/docs/en/permissions). Settings. [Docs](https://code.claude.com/docs/en/settings). Memory, including `CLAUDE.md`. [Docs](https://code.claude.com/docs/en/memory).
- Best practices. [Docs](https://code.claude.com/docs/en/best-practices).
- Headless runs. [Docs](https://code.claude.com/docs/en/headless). Worktrees. [Docs](https://code.claude.com/docs/en/worktrees). Subagents. [Docs](https://code.claude.com/docs/en/sub-agents).
- Claude Code GitHub Actions. [Docs](https://code.claude.com/docs/en/github-actions).
- Effective harnesses for long-running agents. [Engineering](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
- How we built our multi-agent research system. [Engineering](https://www.anthropic.com/engineering/multi-agent-research-system).
- How Anthropic teams use Claude Code. [News](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code).
- Boris Cherny on verifying the Agent SDK with Opus 5.5, Lean, and TLA+. [LinkedIn](https://www.linkedin.com/posts/bcherny_i-used-opus-55-to-formally-verify-the-claude-activity-7508309724598263808-TVJY).

## People the article leans on

- Addy Osmani, "Agentic Verification", 14 October 2026. [Substack](https://addyo.substack.com/p/agentic-verification).
- Simon Willison, quoting Andrej Karpathy, 26 February 2026. [simonwillison.net](https://simonwillison.net/2026/feb/26/andrej-karpathy/).
- Andrej Karpathy, "Verifiability", 17 November 2025. [bearblog](https://karpathy.bearblog.dev/verifiability/).
- "The proof passes. Of what?" [stravica.ai](https://stravica.ai/blog/the-proof-passes-of-what/). Excerpt at design time.
- Simon Willison, "Agentic manual testing". [Guide](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/).

## Codex, Cursor, and the agents.md convention

- AGENTS.md. [agents.md](https://agents.md/).
- OpenAI Codex and `AGENTS.md`. [Guide](https://developers.openai.com/codex/guides/agents-md). Codex cloud. [Docs](https://developers.openai.com/codex/cloud).
- Cursor rules. [Docs](https://cursor.com/docs/context/rules).
- Cursor Bugbot. [Docs](https://cursor.com/docs/bugbot). Cloud agents. [Docs](https://cursor.com/docs/cloud-agent).

## Tools the later modules will use

These are cited now so the syllabus is not a list of brand names without a page. This milestone does not run them in CI.

- Property tests: [proptest](https://proptest-rs.github.io/proptest/intro.html), [Hypothesis](https://hypothesis.readthedocs.io/en/latest/).
- Mutation: [cargo-mutants](https://mutants.rs/), [mutmut](https://mutmut.readthedocs.io/en/latest/).
- Fuzzing: [cargo-fuzz](https://rust-fuzz.github.io/book/cargo-fuzz.html), [libFuzzer](https://llvm.org/docs/LibFuzzer.html).
- Snapshots and a faster runner: [insta](https://insta.rs/docs/), [cargo-nextest](https://nexte.st/).
- Native checks: [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), [clang-tidy](https://clang.llvm.org/extra/clang-tidy/), [Miri](https://github.com/rust-lang/miri), [Kani](https://model-checking.github.io/kani/).
- Benchmarks: [Criterion](https://bheisler.github.io/criterion.rs/book/).

## Reward hacking

Read in full before modules 5–8. The course uses them for the failure mode they document. It does not copy their methods.

- ImpossibleBench. [arXiv:2510.20270](https://arxiv.org/abs/2510.20270).
- Baker and others, monitoring reasoning models for misbehavior. [arXiv:2503.11926](https://arxiv.org/abs/2503.11926).
- Anthropic, natural emergent misalignment from reward hacking. [arXiv:2511.18397](https://arxiv.org/abs/2511.18397). [Research note](https://www.anthropic.com/research/emergent-misalignment-reward-hacking).

## GitHub and the site

- Code owners. [Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
- GitHub Pages from a workflow. [Docs](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
- Merge queue. [Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).
- Zensical, the site generator used here. [Get started](https://zensical.org/docs/get-started/). [Diagrams](https://zensical.org/docs/authoring/diagrams/). [MkDocs compatibility](https://zensical.org/compatibility/). [Publish](https://zensical.org/docs/publish-your-site/).
- Material for MkDocs reaches end of life on 5 May 2027. [Project](https://squidfunk.github.io/mkdocs-material/). Zensical is the successor this course builds with. The theme name in `mkdocs.yml` is still `material`, which is the compatibility path Zensical documents.
