# Lab 3. Audit the three instruction files

The harness under `harness/` is a project root: `CLAUDE.md`, `AGENTS.md`, `REVIEW.md`, `.cursor/rules/verification.mdc`, settings, and the skill. The lab points an auditor at that directory.

## The starter

The starter passes when `CLAUDE.md` exists. A file that exists can still contradict the other two, exceed the Codex cap, or forget to deny edits to itself.

```python
--8<-- "labs/m03/starter/audit.py"
```

## The solution

The solution calls `audit` in the harness library. CI runs it against `harness/` and expects `ok`.

```python
--8<-- "labs/m03/solutions/audit.py"
```

```text
python3 labs/m03/solutions/audit.py harness
```

Read the three copies and check the sentence yourself. The Cursor rule is short:

```markdown
--8<-- "harness/.cursor/rules/verification.mdc"
```

The Codex file includes a Code Review Rules section and the size warning:

```markdown
--8<-- "harness/AGENTS.md"
```

## Walk through a failure you can make on purpose

Copy `harness/` to `/tmp/loose` and delete the done sentence from `/tmp/loose/AGENTS.md`. Run the solution auditor on `/tmp/loose`. It should name `AGENTS.md` and exit 1. Put the sentence back and append 40 KiB of commentary. It should fail on the 32 KiB cap. That second failure is the one people miss, because the file looks fine in an editor and Codex has already stopped reading.

Then open `harness/.claude/settings.json` and find the deny entries and the two hook events. The auditor checks that the deny list mentions both `.verify` and `.claude`, and that `Stop` and `PreToolUse` are registered. It does not prove the hook scripts are correct. That is module 4, with recorded events.

## Exercise

The skill says the agent may fill `E2E` and `NOT CHECKED` only after the runner has written `evidence.md`.

??? success "Why are those lines not the verdict?"

    They are notes a person reads. The verdict is the exit code and the integrity hash in `evidence.json`, which the runner writes and CI can recompute. An agent that writes the notes first, or writes a PASS line instead, is back to grading its own exam. The skill exists so Claude is told that in the place a `/verify` call will load.

## Exercise

You want the agent to be unable to `cat .env`.

??? success "Where does that rule go?"

    In `permissions.deny`, as `Read(.env)`, which the template already has. Putting "do not read .env" only in `CLAUDE.md` is an instruction. The deny rule is the permission. Neither replaces a server-side secret store, and this course's CI has no secrets to leak. The pattern still belongs in the template so the next repo does not learn it the hard way.
