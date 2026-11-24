# Lab 10. Score the report split

The starter treats the word "bug" as a verdict. None of the report-split write-ups use that word for the misses that matter, so the starter exits non-zero. The solution uses the same rule as `tools/reviewer/score.py`: `exit 1` means a bug, and everything else is clean.

```python
--8<-- "labs/m10/starter/decide.py"
```

```python
--8<-- "labs/m10/solutions/decide.py"
```

```text
python3 labs/m10/starter/decide.py tools/reviewer/reviews.json
python3 labs/m10/solutions/decide.py tools/reviewer/reviews.json
python3 tools/reviewer/score.py
```

CI expects the starter to exit non-zero and the solution to exit 0. `score.py` must print the text in `tools/reviewer/expected.txt`, including `tune_excluded 4` and `adversary_rejected 1`.

The bar inside the lab programs is the fixture's own result: at least two true positives on the report split, and no more than one false positive and one false negative. A rubric that flags everything fails that bar. A rubric that flags nothing fails it too.
