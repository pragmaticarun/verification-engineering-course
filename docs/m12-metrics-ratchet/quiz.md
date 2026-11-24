# Quiz 12

### 1

Reads per ship is 2/9. Which rows are the numerator?

??? success "Answer"

    Ships that a person opened. In this file that is `a` and `c`, both merged, both green. The open of `j` is not in the numerator because `j` did not ship. Reads per ship is about shipped changes.

### 2

Why is escape count 2 while catch rate is 2/3?

??? success "Answer"

    Escapes count merged changes that were wrong later, including `d`, which merged green. Catch rate only looks at rows with `check_exit` 1, and two of those three were held. `d` is invisible to catch rate. A green escape needs the escape count.

### 3

Cost is 3.70, not the cost of the nine ships alone. Why add the holds?

??? success "Answer"

    A held change still spent model time, CI time, or a person's time. Leaving holds out of the sum makes a noisy gate look cheap.

### 4

The article says to delete checks that have not fired in 60 days. What does this course do with that sentence?

??? success "Answer"

    It treats 60 as the author's number. The pruner may drop a non-catastrophic check that has been quiet that long. It may not drop `tamper` for the same quiet period. The verification note says to tidy the list. It does not give the number 60.

### 5

A retrospective says "next time, watch for negative peaks." Has the ratchet moved?

??? success "Answer"

    Not until a command fails on a negative peak. `tools/heldout/hidden_cases.json` is that command's input. A sentence in a document is a wish.

### 6

Someone drives reads per ship to 0 by telling reviewers to stop opening green changes. Is the metric better?

??? success "Answer"

    The number is lower. The harness is not better if the unopened changes include an ABI or a lock file. The metric is there so you can ask whether the remaining opens are the ones you meant. Zero is not the goal.
