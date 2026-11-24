# Quiz. The capstone

### 1

Before catch rate is 1/4. Which red row is the one the tick policy catches?

??? success "Answer"

    `p8`, with two ticks and `check_exit` 1. The other red rows have six or eight ticks, so the old policy ships them.

### 2

After reads per ship is 1/4. Is that "better" than 2/6 because it is smaller?

??? success "Answer"

    It is smaller, and in this fixture the shipped set is the green set, so the remaining open is one green ship. Smaller is not the definition of better. Better is the escape count going from 3 to 0 without a rule that refuses every change.

### 3

`p4` does not ship before and does ship after. What did the tick policy get wrong about it?

??? success "Answer"

    `p4` has four ticks and `check_exit` 0. The form was short. The check passed. A policy that only counts ticks blocks finished work and still ships `p1`, which filled the form and failed the check.

### 4

Why does this page not reuse module 12's 2/9?

??? success "Answer"

    Different rows. Module 12's reads per ship includes nine merges from `runs.json`. This page's reads are opens among the rows each policy ships from `sessions.json`. Averaging them invents a number.

### 5

The heavy job runs Miri, cargo-mutants, cargo-fuzz, and one Kani harness. Does `before_after.py` run those tools once per row?

??? success "Answer"

    No. The rows carry an exit code. The heavy job is a separate workflow on the repository. Saying the capstone fuzzed eight agents, or proved them with Kani, would be false.

### 6

What would you replace in the fixture if you had real CI statuses?

??? success "Answer"

    The `check_exit` field, with the status you downloaded, and then `expected.txt`, in the same commit. You would not replace the script with a model's summary of the session.
