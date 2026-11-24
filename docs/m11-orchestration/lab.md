# Lab 11. Refuse a stale hash

The starter admits every session. The fixture has one fresh hash and one stale hash, so the starter exits non-zero. The solution admits a session only when `tree_hash` equals `reviewed_hash`.

```python
--8<-- "labs/m11/starter/admit.py"
```

```python
--8<-- "labs/m11/solutions/admit.py"
```

```text
python3 labs/m11/starter/admit.py labs/m11/fixtures/sessions.json
python3 labs/m11/solutions/admit.py labs/m11/fixtures/sessions.json
python3 tools/orchestrator/run.py
```

CI expects the starter to fail and the solution to exit 0. The orchestrator must print `tools/orchestrator/expected.txt`: six worktrees, three queued, one hold, one stale review, one stale base, budget 8. A ninth session raises `ValueError` before `git worktree add`.

The worktrees live in a temporary directory the script deletes. You do not get a leftover repository, and you do not need a GitHub remote.
