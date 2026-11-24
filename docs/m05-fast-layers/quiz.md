# Quiz 5

### 1

Why does the golden test compare bytes instead of file size?

??? success "Answer"

    Two different clips can have the same length. The sample values are the contract. Size is a cheap filter and it is not the comparison.

### 2

Who is allowed to set `UPDATE_GOLDEN=1`, and what do they still have to do?

??? success "Answer"

    A person who is about to read the diff. The flag rewrites the contract. Accepting it without reading the bytes accepts whatever the current encoder emitted.

### 3

The course cites insta and cargo-nextest. Why are they not in `make fast`?

??? success "Answer"

    They are not installed, so CI does not run them. The lesson shows the golden comparison and the test runner this repo actually executes. Naming a tool you did not run is a citation. Pasting its API as if the suite used it would be a false example.

### 4

What does `pcmkit/fast/flaky_scan.py` reject?

??? success "Answer"

    Calls and markers: `time.sleep`, thread sleeps, pytest and unittest skips, `#[ignore]`, a flaky mark, and the retry-until-green token. It scans `pcmkit/` and `briefs/` in CI. A comment that discusses the policy is not a call.

### 5

The Rust tests of `apply_gain_db` pass and the C++ consumer fails. What did the Rust tests not cross?

??? success "Answer"

    The C ABI. `pcmkit_apply_gain` is a different function from `apply_gain_db`, with a pointer, a length, and a status code. The consumer is the contract test for that boundary.

### 6

Codex will not run clang-tidy by itself. What still runs it?

??? success "Answer"

    `make fast`, which CI runs. An `AGENTS.md` line can tell Codex to run that command. The line is not the run.
