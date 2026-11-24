# Lab 8. Do not let a listening note wear an E2E label

Two transcripts. The honest one is the shape `prove.py` prints. The bluff says someone listened and that this passed.

```text
--8<-- "labs/m08/fixtures/honest.txt"
```

```text
--8<-- "labs/m08/fixtures/bluff.txt"
```

The starter accepts any file that contains an `E2E:` line. The solution accepts only the mechanical line, rejects a second `E2E:` line, and rejects a `NOT CHECKED:` line that contains "passed."

```python
--8<-- "labs/m08/starter/narrate.py"
```

```python
--8<-- "labs/m08/solutions/narrate.py"
```

```text
python3 labs/m08/starter/narrate.py labs/m08/fixtures/bluff.txt
python3 labs/m08/solutions/narrate.py labs/m08/fixtures/bluff.txt
python3 labs/m08/solutions/narrate.py labs/m08/fixtures/honest.txt
```

The starter exits 0 on the bluff. The solution exits 1. The solution exits 0 on the honest file. CI asserts that.

## Run the real command

```text
python3 pcmkit/e2e/prove.py
```

You should see the `E2E:` line and four `NOT CHECKED:` lines, and a zero exit status. If the goldens are missing, the command fails. Do not pass `--update` to silence it unless you mean to change the contract and you are about to read the WAV and the PNG.

`make check` runs this command after the library tests, because it needs the `pcmx` binary. The checks file names the same string, `python3 pcmkit/e2e/prove.py`, so a runner pointed at this repo will execute it when a `pcmkit/` path changes.

## What the runner keeps

`command_notes` in the harness keeps those prefixed lines and drops everything else, including a handwritten `VERDICT: PASS` that happened to be on stdout. The integrity hash still does not cover the notes. A later edit to the markdown cannot repair a non-zero exit, and a forged JSON verdict fails the audit, the way module 4's corpus already checks.

You can see the copy happen by running the runner inside a checkout where the harness sits at the root and the checks file is the course one. In this repository the harness lives in `harness/` and `make check` calls `prove.py` directly. Both are runs. The runner is what adds the tree hash and the integrity line. The direct command is what produces the notes. CI does both: `make check` runs `prove.py`, and the harness tests run the runner on recorded repos.

## Walk through a golden failure

Change one sample in `SAMPLES` inside `prove.py` and run it without `--update`. The exit status is non-zero, and the diff you did not write is the point: the committed WAV is the behavior. Put the sample back. If you were changing the normalizer on purpose, `--update` plus a reviewed diff is the path, and the `E2E` line only returns when the bytes match again.

## Exercise

You listened on headphones. The click is in the source file, not in the normalizer. You want the commit to record that.

??? success "Where does the sentence go?"

    In an `Exemption-reason` trailer next to `Verified-by: none`, if you are skipping a red local gate, or in a human note that does not start with `E2E:`. It does not replace the golden line. The golden line is still true or false independently of your ears. Module 4's hook accepts a substantive trailer locally and CI still runs `prove.py`.

## Exercise

`prove.py` prints `NOT CHECKED: cargo-fuzz was not run`. A teammate deletes that line so the report looks finished.

??? success "What did they remove?"

    A true statement about the limit of this command. The suite did not start cargo-fuzz. Deleting the line does not run the fuzzer. It makes a reader invent a coverage-guided run that never happened. The runner will also stop copying the line, because it only copies what the command prints. Put the line back.
