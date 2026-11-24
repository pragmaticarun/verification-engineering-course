# Quiz 4

### 1

The corrected stop hook exits 0 when it wants the model to keep working. How does Claude Code tell block from allow?

??? success "Answer"

    A JSON `decision` of `block` on stdout keeps the session going. Empty stdout allows the stop. Exit 2 is the other documented block signal. This hook uses the JSON path and reports the code on stderr.

### 2

Why is a `.tries` file inside the repo the wrong counter?

??? success "Answer"

    It is one counter for every session, and the agent can edit or delete it. The corrected counter is outside the worktree, keyed by repository and `session_id`. Another session's file does not increment it.

### 3

`git commit -m "ship" # Verified-by: none` is denied. What would be allowed locally, and what still runs?

??? success "Answer"

    A parsed trailer `Verified-by: none` plus a substantive `Exemption-reason` in the same trailer paragraph. Locked paths, test edits, tamper, and scope still block. CI still runs the checks. The phrase in a comment is not a trailer.

### 4

The worktree's `gate.json` says `"mode": "off"` and the base ref says `enforce`. Which one wins?

??? success "Answer"

    The base ref. The worktree file is also a locked path, so the diff that flipped it is a reason to block on its own. `off` is a human setting on the branch you merge into, used to roll out, not a switch the change carries with it.

### 5

Name a commit-shaped command the hook does not treat as `git commit`, and one it refuses because it cannot see through it.

??? success "Answer"

    `git commit-tree` is not a commit of the index and is ignored by the commit matcher. `git $(echo commit)` hides the verb inside a substitution, and the hook fails closed when it sees `$(` or backticks together with `git` and `commit`.

### 6

The strong ledger property fails the buggy ledger. The weak one holds. What is the difference in the inputs?

??? success "Answer"

    The weak property only deposits, so a ledger that ignores withdrawals stays non-negative. The strong property withdraws the full balance, overdrafts, and withdraws from zero. A property that does not contain a failing input cannot catch a no-op implementation.
