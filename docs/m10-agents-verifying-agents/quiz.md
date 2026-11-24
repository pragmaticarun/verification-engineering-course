# Quiz 10

### 1

Precision on this fixture is 2/3. What is the one false positive?

??? success "Answer"

    The clean write-up that says `HOLD exit 1 because the log looks noisy`. The rule sees `exit 1` and calls it a bug. The label says the change was clean. That is the cost of a rule that trusts the quoted exit more than the prose around it.

### 2

Recall is also 2/3. What is the miss?

??? success "Answer"

    `ship it, looks good`. It names neither `exit 1` nor a failing command. The rule calls it clean. The label says the change was a bug. A confident ship with no exit code is the miss.

### 3

Why is the tune split printed as a count rather than folded into the fraction?

??? success "Answer"

    You are allowed to edit the rubric because of the tune split. If those rows also enter precision and recall, the published number is the rows you fitted. `tune_excluded 4` is the output saying they stayed out.

### 4

A teammate wants a second reviewer that reads the first reviewer's verdict and says whether it "feels right." What does the verification note suggest you do instead?

??? success "Answer"

    Tune the first reviewer. The note's report is that a second, more expensive pass often rubber-stamps the first. This module's measurement is one rule on a labeled split.

### 5

Can you quote Baker and others' 95% recall next to `precision 2/3`?

??? success "Answer"

    Only as their result, on their two hacks, with their monitor. This script's 2/3 is six mocked strings and a substring rule. The two numbers are not comparable, and the script never called GPT-4o.

### 6

The adversary rejects a test proposal whose samples are `0.2` and `0.4` for a sign bug. Why is that proposal a fail even if the tests pass?

??? success "Answer"

    A sign bug is invisible on non-negative samples. A passing proposal that cannot produce a negative sample is the visible suite from module 9. The proposal that includes `-0.4` is the one the script keeps.
