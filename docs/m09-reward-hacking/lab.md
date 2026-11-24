# Lab 9. A peak the visible cases cannot see

The starter takes the largest sample. Every visible case is `>= 0`, so the starter passes that file. The hidden cases include negatives. The solution takes the largest absolute sample.

```python
--8<-- "labs/m09/starter/peak.py"
```

```python
--8<-- "labs/m09/solutions/peak.py"
```

```text
python3 labs/m09/starter/peak.py tools/heldout/visible_cases.json
python3 labs/m09/starter/peak.py tools/heldout/hidden_cases.json
python3 labs/m09/solutions/peak.py tools/heldout/hidden_cases.json
```

The starter exits 0 on the visible file and non-zero on the hidden file. The solution exits 0 on both. CI asserts that split. The course command that locks the split in one process is `python3 tools/heldout/run.py`. Its stdout is the fixture `tools/heldout/expected.txt`.

## What you are not doing

You are not hiding the hidden file from yourself. You are checking that a checker which only had the visible file is a different program from the one CI runs. The mock agent never receives `tools/heldout/` because `tools/mockagent/repo.py` copies `harness/` and nothing else.

## The owners file is still a template

Read `harness/platform/CODEOWNERS`. It names the three paths a code owner should have to approve. It is not at `.github/CODEOWNERS`, and `@course-maintainers` is not a team in this repository. Copying the three lines to `.github/CODEOWNERS` still does nothing until the ruleset requires code-owner review. The lab does not ask you to apply that setting.
