# Project 1. Your own reads-per-ship

About ninety minutes. You finish with a second fixture and a number you can explain.

## Do this

1. Copy `labs/m01/fixtures/reviews.json` to a file outside the repo, or under `/tmp`. Do not replace the fixture CI uses.
2. Add four rows from a morning you remember, or from a morning you invent and label as invented. Use the same fields: `id`, `ticks`, `check_exit`, `human_opened`. Include at least one row with many ticks and a failing check, and one row with a passing check that nobody opened.
3. Run the solution against your file:

    ```text
    python3 labs/m01/solutions/review.py /tmp/my-reviews.json
    ```

4. Write five lines in a note:
    - how many the starter would ship
    - how many the solution ships
    - the reads-per-ship figure
    - one row you would still open even though the check passed, and why (auth, a migration, a format change a listener would hate)
    - one command in `pcmkit` you already trust more than a checklist (the unit tests, the oracle, or the C++ consumer)

## Done when

The solution prints `HOLD` for every row whose `check_exit` is not 0, and your note names a `pcmkit` command. You do not need a model, and you do not commit the personal fixture. The course fixture stays the one under `labs/m01/fixtures/`.

## Where this shows up again

Module 2 turns "I trust the normalize command" into a brief that names the command before the code is written. Module 12, when it lands, will compute this ratio from trailers instead of from a hand-built JSON file.
