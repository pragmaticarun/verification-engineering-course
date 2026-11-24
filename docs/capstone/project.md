# Project. Publish the before and after

About two hours. You finish with the ten lines from the script and a short note that says what you did not measure.

## Do this

1. Run `python3 tools/capstone/before_after.py` and `python3 tools/orchestrator/run.py`. Paste both outputs.
2. In one paragraph, say what the tick policy shipped that the exit-code policy held. Name the row ids.
3. In one paragraph, say what the exit-code policy shipped that the tick policy held. `p4` is the interesting one. Explain why that is not a regression.
4. Add a "Not checked" section of your own, at least four lines. Include: no live model, the GitHub ruleset is not applied, the merge queue is not enabled, and the heavy fuzz and mutant runs are smokes with a time box rather than a campaign. If you did not listen to a WAV this week, say that too.
5. Re-run `make check` if you changed a fixture. If you changed nothing, say that the committed `expected.txt` is the result you are standing behind.

## Done when

A reader can regenerate the ten lines and can tell this fixture from module 12's week. The not-checked section is present. The course's own not-checked list, on the setup page and in the heavy workflow, should not be contradicted by yours.

Back to the [syllabus](../syllabus.md).
