# Quiz 2

### 1

Which line makes a brief executable?

??? success "Answer"

    `command:` together with `expect_exit:`. A goal paragraph explains the command. It does not replace it.

### 2

The starter accepts `labs/m02/fixtures/vague.md`. Why is that a bug in the starter and not a success of the brief?

??? success "Answer"

    The starter only checks the title line. The vague brief has a title and does not name a command, an exit status, or a path. A linter that passes it will pass every agent prompt someone pasted under a heading.

### 3

Why is "leave exact silence unchanged" in the goal and not only in a unit test the agent might write later?

??? success "Answer"

    Peak normalization divides by the peak. Silence has a peak of zero. If the goal does not mention it, a brief-shaped agent can divide, produce NaN, and test only the loud files. The acceptance script in this repo checks silence because the brief required it.

### 4

Non-goals include "no sample-rate conversion." The agent converts anyway and the peak is 1. Did the brief pass?

??? success "Answer"

    No. The peak check can pass while a non-goal was violated. The allowed-file list is what makes that visible when the conversion had to touch a file outside the list. If you allowed every file, you lost the signal, and you need a check that the rate bytes did not change.

### 5

The lint looks up acceptance paths that contain a slash or end in `.py` or `.sh`. What does it not prove?

??? success "Answer"

    That the command tests the goal. A script can exist, exit 0, and assert nothing. Existence is the cheap check. Reading the script is still yours, once, when you write the brief.

### 6

Codex and Cursor can both open `BRIEF.md`. What do they not do with it unless you add a check?

??? success "Answer"

    They do not reject a vague brief, and they do not block a diff outside Allowed-files. The lint and the scope gate do those jobs. The instruction files only tell the tool to stay inside the list.
