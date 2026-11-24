# Quiz 8

### 1

What does `prove.py` compare, besides a peak number?

??? success "Answer"

    The normalized WAV bytes and the waveform PNG bytes, against files in `pcmkit/golden/`. The peak check is an extra guard. The goldens are the contract.

### 2

Why is listening a `NOT CHECKED` line and not an `E2E` line?

??? success "Answer"

    This process cannot hear. `E2E` is reserved for the command that ran. A person who listened can say so in a trailer or a note. Putting "it passed" on an `E2E` line is the bluff.

### 3

Are the copied notes part of the evidence integrity hash?

??? success "Answer"

    No. The hash covers the verdict, the problems, the commands, the producer, and the tree hash. The notes are for a person. Forging the verdict still fails the audit. Editing a note does not make a failed command pass.

### 4

`prove.py` does not print a skip count. What should you not write into `evidence.md` by hand?

??? success "Answer"

    `SKIPPED: 0`, or any count this command did not measure. The Rust suite is a different check. A blank narrative is not a claim that nothing was skipped.

### 5

The starter accepts `bluff.txt`. What did it fail to read?

??? success "Answer"

    The words after `E2E:`. Any line with that prefix was enough. The solution requires the golden sentence and rejects a listening line dressed up as the end-to-end result.

### 6

Codex does not load the verify skill. How does this module still apply?

??? success "Answer"

    The command and the runner are ordinary programs. `AGENTS.md` can name them. CI runs them without a skill. The skill is a reminder for Claude, not the lock.
