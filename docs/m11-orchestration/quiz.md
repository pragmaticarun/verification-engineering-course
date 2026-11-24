# Quiz 11

### 1

Three rows queue. What do the other three fail, one each?

??? success "Answer"

    `a3` has `check_exit` 1, so it is held. `a4` was reviewed against a hash that is not the file, so it is stale. `a5` was reviewed against a base that is not `HEAD`, so the base is stale. A queue of six would mean the script ignored all three.

### 2

Why is the mock one process instead of six model calls?

??? success "Answer"

    So CI can replay the decisions with no API key and no network. A live orchestrator would be one agent per worktree. The lesson's claim is about the decisions, not about having talked to a model.

### 3

The budget is 8. Module 4's platform cap is also 8. Are they the same control?

??? success "Answer"

    No. Module 4 caps how many times one session may be continued after a blocked stop. This module caps how many sessions you start. Reusing the number is a memory aid. It is not one setting.

### 4

A review was correct at 10:00. `main` moved at 10:05. You merge the review. What did you merge?

??? success "Answer"

    A review of the old base. The `stale-base` row is that mistake. A merge queue exists to re-run checks on the updated base. This course does not enable GitHub's merge queue. The script only refuses the row.

### 5

Two agents both edit `clamp.rs` in two worktrees. Is the isolation a pass?

??? success "Answer"

    It is isolation. You have two commits instead of one tangled checkout. Each commit still has to go through the gate. A worktree does not review itself.

### 6

Headless Claude Code, Codex cloud, and Cursor cloud agents are on the references page. Which of them does `run.py` start?

??? success "Answer"

    None. They are the products you would point at a worktree if you were spending a key. The script uses `git worktree add` and a fixture.
