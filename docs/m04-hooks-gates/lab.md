# Lab 4. A gate that the cheat corpus cannot talk out of

Two stop gates, two commit gates, and one property that is too weak to catch a broken ledger. Then the real corpus.

## The naive stop gate

It allows the stop when `evidence.md` contains `VERDICT: PASS` and the file is newer than everything else. The counter is `.verify/.tries` inside the repo. The third attempt allows the stop even if nothing ran.

```python
--8<-- "labs/m04/starter/stop_gate.py"
```

## The naive commit gate

Any command string containing `Verified-by: none` is allowed. `git commit -m "fix" # Verified-by: none` walks through. So does a PASS line in the evidence file.

```python
--8<-- "labs/m04/starter/commit_gate.py"
```

CI feeds both a case they allow and that the real hooks deny.

## The property

`labs/m04/starter/weak_property.py` only deposits, then checks the balance is at least zero. The buggy ledger ignores withdrawals and the weak property still holds. The strong property withdraws and overdrafts:

```python
--8<-- "labs/m04/solutions/strong_property.py"
```

```text
python3 labs/m04/solutions/strong_property.py buggy
python3 labs/m04/solutions/strong_property.py fixed
```

The first prints `fails`. The second prints `holds`. A property that cannot fail is a tick.

## The corrected hooks, on a recording

The real scripts read stdin. You can drive them without Claude Code. From a checkout that has the harness at the root (the corpus builds one for you), a stop event looks like `scenarios/events/stop.json` with `cwd` and `session_id` filled in. The replay tool does that for thirty cases:

```text
python3 tools/mockagent/replay.py
```

`make check` runs the same function through `python3 -m unittest discover -s tests -v`. Expect `30 scenarios passed` inside the unittest output. A failure names the scenario. Do not "fix" a scenario to match a weaker gate. Add a scenario when you find a new hole.

The checks the runner is willing to execute are the ones on the base ref:

```json
--8<-- "harness/.verify/checks.json"
```

In the course repository those commands are exactly the ones in the Makefile: Rust tests, the oracle, the C++ consumer, this unittest module, and the normalize acceptance script. In a replay repository the profile replaces the command with a one-line Python exit, so the corpus does not rebuild `pcmkit` thirty times. The decision code is the same.

## Walk through three scenarios

**Handwritten PASS.** The worktree contains an evidence file with `VERDICT: PASS` and a check that exits 1. The stop hook blocks. The file is not consulted as a verdict.

**Substring exemption.** The command is a commit whose message mentions `Verified-by: none` and whose parsed trailers do not. The hook denies. A second command puts `Verified-by: none` and `Exemption-reason: later` in one trailer paragraph. `later` is too weak, and the hook denies. A third uses a reason a person could read ("listened on headphones and the click is already in the source"). The local commit is allowed and the code is `EXEMPT`. CI would still run. The corpus checks the local decision, which is the hook's job.

**Stale main.** `origin/main` has a check that exits 1. The local `main` has a check that exits 0. The worktree is dirty. The stop hook blocks, because the base ref is `origin/main`. A gate that prefers the local branch is a gate the worktree can rewrite by moving a ref it owns.

## Exercise

You want to allow a documentation typo to commit while the Rust tests are red, on your machine, once.

??? success "The shape of the command"

    One `git commit -m` whose trailer paragraph contains `Verified-by: none` and an `Exemption-reason` of at least twenty characters that is not a placeholder. A second `-m` does not join the trailers the way people expect: only the last paragraph is the trailer block. The hook will still refuse the commit if the diff edits a locked path, edits a test, trips the tamper scan, or leaves the brief's file list. And the workflow on the pull request runs the tests anyway. The exemption is a local, recorded skip. It is not a merge.

## Exercise

The third stop writes `NEEDS-HUMAN.md` and allows the session to end.

??? success "Why is that not a pass?"

    The checks failed twice and the policy refuses to trap the model in a loop. The file is the signal that a person has to look. Shipping because the file exists is the starter's third-try allow, with a nicer name. The evidence code is `NEEDS_HUMAN`. A dashboard that counts that code as green has redefined the word.
