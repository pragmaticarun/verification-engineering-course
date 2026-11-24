# Lab 12. Keep the quiet lock

The starter deletes every check that has been quiet for 60 days or more. The fixture's tamper check has been quiet for 90 days and is marked catastrophic, so the starter drops it and exits non-zero. The solution keeps a catastrophic check however long it has been quiet, and still drops `format`.

```python
--8<-- "labs/m12/starter/prune.py"
```

```python
--8<-- "labs/m12/solutions/prune.py"
```

```text
python3 labs/m12/starter/prune.py labs/m12/fixtures/checks.json
python3 labs/m12/solutions/prune.py labs/m12/fixtures/checks.json
python3 tools/metrics/report.py
```

CI expects the starter to fail, the solution to exit 0, and the report to match `tools/metrics/expected.txt`. The report's prune line is `pruned format` and the kept line includes `tamper`.

Sixty days is the window under discussion. It is not a measurement this repository produced.
