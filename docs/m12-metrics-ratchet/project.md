# Project 12. Turn one miss into a check

About two hours. You finish with the nine-line report and one new check you could add, written as a command rather than a slogan.

## Do this

1. Run `python3 tools/metrics/report.py`. Paste the nine lines into the note unchanged.
2. Pick one miss this course already turned into a check: the negative peak, the toward-zero mutant, the listening bluff, or the stale review. Write the command CI runs for it, and the row in the report that would have stayed green without that command.
3. Propose one prune and one refusal. The prune has to be a check whose failure would be obvious another way. The refusal has to be a check you would keep through 90 quiet days, with the reason a failure would be quiet in production.
4. Recompute reads per ship from `tools/metrics/runs.json` by hand. If you get a fraction other than 2/9, you counted an unshipped open or you missed a ship. Fix the count before you write the sentence.
5. Do not delete `tamper` from `harness/.verify/checks.json` to see the dashboard move. The lab already shows that deletion failing.

## Done when

The note contains the fixture's fractions, one command that exists because of a miss, and one check you would not prune. The 60-day window is labeled as the author's number.

Next: the [capstone](../capstone/index.md).
