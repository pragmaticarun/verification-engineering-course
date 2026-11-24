# Lab 5. Same length is not the same clip

Two files, four bytes each, different contents. The starter compares the lengths. The solution compares the bytes.

```python
--8<-- "labs/m05/starter/compare.py"
```

```python
--8<-- "labs/m05/solutions/compare.py"
```

```text
python3 labs/m05/starter/compare.py labs/m05/fixtures/left.bin labs/m05/fixtures/right.bin
python3 labs/m05/solutions/compare.py labs/m05/fixtures/left.bin labs/m05/fixtures/right.bin
```

The starter exits 0. The solution exits 1. CI asserts both. The real golden in `pcmkit` is the same idea aimed at a WAV and a PNG:

```rust
--8<-- "pcmkit/crates/pcmkit/src/course_checks.rs"
```

The first test in that file is the one `cargo test` runs on every `make fast`. The rest of the file belongs to modules 6 and 7, and it lives here so one `cargo test` is the fast tier's Rust half.

## A sleep is not a fast test

```python
--8<-- "labs/m05/fixtures/sleepy.py"
```

```text
python3 pcmkit/fast/flaky_scan.py labs/m05/fixtures/sleepy.py
```

That exits 1. The same scanner on `pcmkit` and `briefs` exits 0, and `make fast` requires the exit 0.

## Walk through the consumer

`bash pcmkit/cpp/run_consumer.sh` builds the static library and the C++ caller. Read `pcmkit/cpp/tests/consumer.cpp` and name the check that would fail if a NaN gain zeroed the buffer. The gain function promises to check the input before it writes. The consumer is the program that holds it to that promise across the ABI. A Rust unit test of `apply_gain_db` does not call `pcmkit_apply_gain`.

Then run the linters the workflow runs:

```text
bash pcmkit/fast/python_lint.sh
bash pcmkit/cpp/run_tidy.sh
```

`python_lint.sh` is ruff and mypy, pinned. `run_tidy.sh` is clang-tidy with `bugprone-*` and `clang-analyzer-*`, not the wider `.clang-tidy` file sitting next to it. The script's `--config` replaces that file for the CI invocation. If you turn the wider file on, you own the new findings. Do not describe the wider file as what CI runs.

## Exercise

You want a golden for a new 24-bit export.

??? success "The shape of the change"

    Add a fixed buffer, encode it, and compare to a new file under `pcmkit/golden/`. Generate the file once with `UPDATE_GOLDEN=1`, look at the diff, and commit the bytes. A test that only checks the file exists, or only checks the length, is the starter. The format is part of the contract: a 24-bit file that is the right size and the wrong samples is a broken export.

## Exercise

Clippy starts taking two minutes because someone enabled a lint that type-checks the world three times.

??? success "Where does that lint go?"

    Out of `make fast`. A lint you need and cannot make cheap belongs in the heavy workflow, with a time limit, and the lesson should say the light job does not run it. Leaving it in the fast tier trains everyone to skip the tier.
