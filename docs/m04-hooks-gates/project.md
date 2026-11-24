# Project 4. Add one scenario

About two hours. You finish with a recorded event that the current gate already classifies the way you expect, and a note about a cheat you did not try to make the gate miss on purpose.

## Do this

1. Read `tools/mockagent/replay.py` far enough to see how a scenario calls the stop hook or the commit hook. Do not change the existing thirty.
2. In `/tmp`, write one extra JSON event. Start from `scenarios/events/stop.json` or `scenarios/events/pretool_commit.json`. Change `last_assistant_message` or the command so the story is yours. A useful one: a commit that adds a brand-new test file and does not touch an old one. The policy allows that.
3. Run the stock corpus and confirm it still passes:

    ```text
    python3 tools/mockagent/replay.py
    ```

4. If you wire your event into a private copy of the replay script under `/tmp`, assert the decision code you expect. If you are not ready to wire it, run the hook by hand against a temp repo built the way `make_repo` does, and write down the code you observed (`PASS`, `BLOCK`, `EXEMPT`, `NEEDS_HUMAN`, or a deny).
5. Write five lines: the hole from the list of ten your event is closest to, the code you observed, what CI would still run, which tool the hook does not see, and one cheat you will not claim is covered (a held-out test the agent cannot read is module 9, and it is not in this corpus).

## Done when

The stock corpus passes, and your note names a decision code you actually saw. Do not weaken a scenario to get a green run. The files CI executes stay as they are.

You now have the first four modules: a reason to prefer an exit code, a brief that names the command, instruction files that agree, and a gate you can replay. Modules 5–12 and the capstone are on the [syllabus](../syllabus.md). They are the layers that make the exit code hard to fake, and the measurement at the end.
