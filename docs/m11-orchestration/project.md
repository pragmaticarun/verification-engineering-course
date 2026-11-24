# Project 11. Draw your own six rooms

About two hours. You finish with a table of six changes from this course, each marked queue, hold, stale, or stale-base, using the rule in `decide`.

## Do this

1. Run `python3 tools/orchestrator/run.py`. Confirm the seven lines match `tools/orchestrator/expected.txt`.
2. Pick six real commands you have run in this course (`cargo test`, the oracle, the held-out script, a unit test you know fails, and two you invent as "reviewed yesterday"). Assign each a fictional tree hash and a base. At least one hash must be stale. At least one base must be stale. At least one exit code must be non-zero.
3. Apply `decide` by hand. Write the four counts.
4. Say what you would refuse to parallelize even with worktrees. Payments, auth, and anything that deletes are the usual answers. "All of pcmkit" is also allowed if you say why the checks are not enough for that change.
5. Do not start a cloud agent. If your note describes a live run, it is about a different exercise than this one.

## Done when

The table has six rows and the same four outcomes the script knows. A reader can recompute the counts. The note says the GitHub merge queue is not enabled here.

Next: [module 12](../m12-metrics-ratchet/index.md).
