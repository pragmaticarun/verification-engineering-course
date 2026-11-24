# Lab. Stop shipping red checks

The starter ships a row with at least six ticks. Several of those rows have `check_exit` 1, so the starter exits non-zero. The solution ships only when the check exited 0, and it still ships at least one green row, so an empty policy does not pass.

```python
--8<-- "labs/capstone/starter/policy.py"
```

```python
--8<-- "labs/capstone/solutions/policy.py"
```

```text
python3 labs/capstone/starter/policy.py tools/capstone/sessions.json
python3 labs/capstone/solutions/policy.py tools/capstone/sessions.json
python3 tools/capstone/before_after.py
```

CI expects the starter to fail, the solution to exit 0, and `before_after.py` to match `tools/capstone/expected.txt`. `before_escapes 3` and `after_escapes 0` are the two lines to be able to say out loud.
