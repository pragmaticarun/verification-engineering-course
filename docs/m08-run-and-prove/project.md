# Project 8. A note a stranger can audit

About two hours. You finish with one `prove.py` run and a six-line record that matches its stdout.

## Do this

1. Run `python3 pcmkit/e2e/prove.py`. Save the stdout.
2. Write six lines:
    - the command
    - the exit status
    - the `E2E:` line, copied
    - the `NOT CHECKED:` lines, copied
    - one thing a tree hash would change if you edited the golden and did not rerun
    - where a listening comment would go if you had listened, and where it would not go
3. Feed your six lines through `labs/m08/solutions/narrate.py` only if you kept the required `E2E` sentence intact. If you paraphrased it, the solution should reject the file. That rejection is correct. Copy the line. Do not improve it.
4. Run `python3 labs/m08/solutions/narrate.py labs/m08/fixtures/bluff.txt` and confirm it still rejects the bluff. Your project does not get to weaken that fixture.
5. Optional: from a scratch repo built the way `tools/mockagent` builds one, run `verify_runner` and find the narrative section. If you skip this, say so. Do not describe a tree hash you did not print.

## Done when

A reader can replay the command and diff your note against the stdout. The note names listening as not checked. Modules 9 through 12 are the lock, the second agent, the worktrees, and the counts. The capstone is the before and after.

Back to the [syllabus](../syllabus.md).
