# Lab 2. A brief the linter can reject

Two briefs, two linters. The vague brief is what you get when "make it louder" is copied into Markdown. The real brief is `briefs/gain-normalize/BRIEF.md`.

```markdown
--8<-- "labs/m02/fixtures/vague.md"
```

## The starter

The starter checks that the first line begins with `# Brief:`. The vague file passes. A title is not a definition of done.

```python
--8<-- "labs/m02/starter/brief_lint.py"
```

```text
python3 labs/m02/starter/brief_lint.py labs/m02/fixtures/vague.md
```

CI asserts the starter exits 0 on that file.

## The solution

The solution calls `lint_brief` from the harness. Empty sections, a missing command, a missing exit status, a non-goal that is not a bullet, and an acceptance path that does not exist are all failures.

```python
--8<-- "labs/m02/solutions/brief_lint.py"
```

```text
python3 labs/m02/solutions/brief_lint.py labs/m02/fixtures/vague.md
python3 labs/m02/solutions/brief_lint.py briefs/gain-normalize/BRIEF.md
```

The vague file exits 1 and names the problems. The normalize brief prints `ok`. Then run the command the brief names:

```text
python3 briefs/gain-normalize/accept.py
```

`make check` runs that command after the Rust tests, because the acceptance test shells out to `pcmx`.

## Walk through a rejection

The vague acceptance section has no `command:` line and no `expect_exit:` line. The non-goals section has a bullet, so that particular check happens to pass, and the allowed-files section has a bullet too. Passing those two is not a pass. The linter returns every problem it finds. A brief that says "whatever needs editing" is a legal bullet and a useless scope. The lint cannot know that the words are vague. You can. The gate will later treat that bullet as the allow list, and then every path matches nothing useful, or you will have written a glob so wide that the list stopped meaning anything. Write paths.

## Exercise

You want a brief for "reject a WAV whose sample rate is 0."

??? success "One acceptable shape"

    Title line, a goal that names the error on a zero rate and says a 48 kHz file is unchanged, an acceptance command that feeds both files to something like `pcmx info` and exits 0 only on that split, a non-goal that says you are not adding a new container, and an allowed-files list that points at the WAV reader and the new test. If the command's script does not exist yet, the lint will say so. Add the script first, even if the assertion is still the one you expect to fail. A brief that points at a missing file is not ready to hand to an agent.

## Exercise

The normalize brief lists `audio.rs`, `main.rs`, and the acceptance script. The agent also edits `wav.rs` to "be helpful."

??? success "Is the normalize command allowed to pass?"

    The command might pass. The change is still not done. Scope is a separate check from the acceptance exit code. A green command on a diff that left the allowed list is the case the article's table named and did not implement. Module 4's scope scenario is that case, with a file outside `src/lib.py` on a brief that only allows `src/lib.py`.
