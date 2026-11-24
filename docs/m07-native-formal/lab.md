# Lab 7. One sample is not a range

The starter calls a function "proved" when `f(0.5) <= 1`. The broken function returns 1 for 0.5 and `sample * 1000` otherwise. The starter accepts it. The solution walks every i16 code.

```python
--8<-- "labs/m07/starter/range_check.py"
```

```python
--8<-- "labs/m07/solutions/range_check.py"
```

```text
python3 labs/m07/starter/range_check.py broken
python3 labs/m07/solutions/range_check.py broken
python3 labs/m07/solutions/range_check.py clamped
```

The starter exits 0 on `broken`. The solution exits 1. On `clamped`, the solution exits 0. The Rust twin is `every_i16_code_stays_in_range_at_the_gain_grid` in `course_checks.rs`, and `cargo test` runs it in the light job. It finished in a small fraction of a second when this lesson was written. Exhaustive over 16-bit codes is cheap. Exhaustive over `f32` is not, which is why a model checker exists and why we do not pretend the grid is that checker.

## The sanitizer binary

```bash
--8<-- "pcmkit/cpp/run_sanitizers.sh"
```

```text
bash pcmkit/cpp/run_sanitizers.sh
```

You should see the consumer print `ok`. Read the script's comment before you write "ASan clean" in a pull request. The C++ side is instrumented. The Rust static library was built with stable `rustc` and no sanitizer flag. A bug that never executes in the C++ file will not show up here.

The consumer's new checks, a NaN gain and a NaN sample, are part of the contract from module 5. The sanitizer run executes them. It does not replace them. UBSan does not know that a NaN gain was supposed to leave the buffer alone. The explicit comparisons do.

## Miri, if you want to see the heavy job locally

The workflow pins the nightly. Locally, after that toolchain is installed:

```text
cargo +nightly-2026-11-23 miri setup
cargo +nightly-2026-11-23 miri test --manifest-path pcmkit/Cargo.toml -p pcmkit --lib miri_gain_of_zero_is_finite
```

The filter is the substring `miri_gain_of_zero_is_finite`. Do not pass `--exact` with that substring. The full test name is `course_checks::miri_gain_of_zero_is_finite`, and an exact filter on the short name runs nothing and still exits 0. An empty pass is a quiet way to skip the test. CI uses the substring, on purpose.

## Exercise

You add a Kani harness in a comment: `// kani::proof gain never overflows`.

??? success "What would have to be true before the comment is a result?"

    Kani would have to be installed, pinned, and executed in CI, and the harness would have to be the property you mean, on the function you mean. A comment is not a run. This repository does not install Kani. The result you have is the i16 grid. Cite that.

## Exercise

Miri is green on `miri_gain_of_zero_is_finite`. The parser smoke has never been run under Miri.

??? success "What can you say?"

    Zero dB on four finite samples did not trip Miri on that nightly. You cannot say the parser is free of undefined behavior, and you cannot say the FFI is. If you want the parser under Miri, add it to the heavy job with a time limit and watch the runtime. Do not append "and the rest of the crate" to a one-test log.
