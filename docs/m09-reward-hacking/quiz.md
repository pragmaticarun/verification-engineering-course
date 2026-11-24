# Quiz 9

### 1

Read-only tests stopped the agent from editing `test_gain.py`. The suite is green. Are you done?

??? success "Answer"

    Not from that fact alone. ImpossibleBench's read-only setup still allowed special-casing on a test name and an equality overload. The tamper scan looks for those added lines. A green suite the agent can see is not a held-out suite.

### 2

The worktree's `gate.json` says `"mode": "off"`. The stop hook blocks. Why is that not a bug in the hook?

??? success "Answer"

    The mode that counts is the one on the base ref. The scenario `gate-mode-off-in-worktree` is the regression. A hook that read the worktree copy would be the bug.

### 3

`pytest.skip` is added, and the commit message carries `Test-change-approved` with a real reason. Should the commit land?

??? success "Answer"

    No. The trailer permits an edit of an existing test. It does not permit a silent skip. `skip-added` is the scenario that locks that.

### 4

Someone commits the hidden cases into the agent's worktree "so the agent can debug them." What did they give away?

??? success "Answer"

    The second key. The agent can now special-case those inputs the way it could special-case a visible test. Held-out only works while the agent does not have the file. CI still has it.

### 5

`harness/.github/ruleset.json` is on `main`. Is the exam locked?

??? success "Answer"

    No. That file is a request. GitHub locks the branch when a ruleset or branch protection with those status checks is applied in the repository settings. This course does not apply it. Local hooks are not the lock either.

### 6

The paper says GPT-5 cheats on 54% of one set of ImpossibleBench tasks. Do you quote that as this repo's catch rate?

??? success "Answer"

    No. That is ImpossibleBench's reported figure for a model on their tasks. This repo's corpus is 30 hand-written scenarios, and the held-out script is two peak cases. Quote the paper for the paper. Quote `tools/heldout/expected.txt` for the peak.
