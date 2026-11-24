# Project 9. Write down where the lock actually is

About two hours. You finish with a one-page note a teammate can use to see which locks are real on a repository they control.

## Do this

1. Run `python3 tools/heldout/run.py` and `python3 -m unittest tests.test_corpus -v`. Record both exit codes. The corpus takes about a minute.
2. List five cheats from the corpus table in the lesson, each with its scenario name and the code you observed (`BLOCK`, `PASS`, `EXEMPT`, `NEEDS_HUMAN`, or whatever the test printed).
3. Open `harness/.github/ruleset.json` and `harness/platform/CODEOWNERS`. For each, write one sentence: what it would do if GitHub were enforcing it, and the fact that this repository has not been switched to that enforcement in this course.
4. Name one path you would add to the code-owner template for a media app you actually ship, and why a quiet failure there is worse than a format failure.
5. Do not create a real GitHub ruleset as part of this write-up unless you are the owner and you mean to. If you do, say which repository and which check names. If you do not, the sentence is "not applied."

## Done when

A reader can tell a local hook from a server rule, and can point at the command that fails `max(samples)` on a negative peak. The note does not say the ruleset is on.

Next: [module 10](../m10-agents-verifying-agents/index.md).
