# Project 10. Label six of your own, then don't score them

About two hours. You finish with six mocked write-ups in the same shape as `tools/reviewer/reviews.json`, and a sentence that says you did not add them to the report split.

## Do this

1. Run `python3 tools/reviewer/score.py`. Copy the five lines. Do not round 2/3 into a percentage in the note. The fixture prints a fraction so the arithmetic stays visible.
2. Write three bug write-ups and three clean ones from pcmkit work you have actually seen in this course: a red `cargo test`, a green oracle, a skip, a special case, a real ship, a bluff. Mark all six `"split": "tune"`.
3. Run them through `labs/m10/solutions/decide.py` only after you wrap them in the same JSON shape, or score them by hand with the `exit 1` rule. Record true positives, false positives, and false negatives.
4. If your tune rows suggest a better rule, write the rule down. Do not edit `tools/reviewer/score.py` to chase them. The report split is the published number, and changing it to fit your six rows is the failure this module is about.
5. State one incident your rule would still miss. That sentence is the start of module 12's "a miss becomes a check."

## Done when

The note shows the fixture's 2/3 beside your tune counts, and it says the tune counts are not the result. No API key appears in the note.

Next: [module 11](../m11-orchestration/index.md).
