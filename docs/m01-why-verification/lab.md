# Lab 1. Ten reviews, two policies

The fixture is ten mocked pull requests. Each row has an id, a count of checklist ticks, the exit code of the real check, and whether a person opened the diff. Nothing here calls a model. The file is the recording.

```json
--8<-- "labs/m01/fixtures/reviews.json"
```

## What the starter does

The starter ships a change when the tick count is at least 6. That is the article's failure, made executable: the checklist is the grade.

```python
--8<-- "labs/m01/starter/review.py"
```

Run it:

```text
python3 labs/m01/starter/review.py labs/m01/fixtures/reviews.json
```

`pr01` has six ticks and `check_exit` 1. The starter prints `pr01 SHIP`. CI asserts that. The starter is supposed to be wrong. If you "fix" the test so the starter looks good, you have graded the exam with the student's pen.

## What the solution does

The solution ships only when `check_exit` is 0. It then counts, among those ships, how many a person opened.

```python
--8<-- "labs/m01/solutions/review.py"
```

```text
python3 labs/m01/solutions/review.py labs/m01/fixtures/reviews.json
```

You should see `pr01 HOLD` and a reads-per-ship line of `0.333`. Six ships, two of them opened.

## Walk through one row

`pr06` has six ticks, exit 0, and nobody opened it. Both programs ship it. The programs agree, and that is fine. The point of a check is that the boring pass does not need you.

`pr07` has six ticks, exit 1, and nobody opened it. The starter ships it. The solution holds it. That row is the afternoon you lost: a ticked list, a failing command, and no person in the loop. A harness exists so this row cannot merge. The starter is the world without one.

`pr04` has a single tick and a passing check. The starter holds it because the checklist looks thin. The solution ships it. Verification is also the right to trust a short diff when the command covered the risk. Hoarding reviews is not care. It is the bottleneck the numbers were about.

## Exercise

`pr08` has two ticks, a failing check, and a person who opened it. The solution holds it. Suppose the person opened it, decided the failure was a known flake, and merged anyway.

??? success "What should the record contain?"

    A trailer or a note that names the flake and the reason, and a failing check that is still visible. The exit code does not become 0 because someone was tired. Module 4's exemption is this idea for a commit hook: `Verified-by: none` only counts as a parsed trailer with a reason, and CI still runs. Silently treating "a person looked" as a pass is the starter, one step later.

## Exercise

Add nothing to the fixture yet. On paper, split the ten rows into shipped-by-the-solution and held.

??? success "Which opened rows are not part of reads per ship?"

    `pr01`, `pr02`, and `pr08` were opened and held, because the check failed. They are attention you spent, and they are not in the ratio, because the ratio is among ships. `pr03` and `pr09` were opened and shipped. Those two are the numerator. If you want a second number, count "opens per review" separately. Do not mix it into reads per ship or the ratio stops meaning what the verification note uses it for.
