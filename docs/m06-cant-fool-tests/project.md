# Project 6. A property that can fail

About two hours. You finish with one new assertion that is false of a mutant you can name.

## Do this

1. Pick `mix` or `resample_linear` in `pcmkit`. Write a fixed-seed property in the same style as `i16_encoding_is_idempotent_on_a_fixed_seed`: a few dozen draws, no new crate, every failure deterministic.
2. Name a one-line bug that property would miss. Example shapes: "the mix is at most 1" misses a mix that always returns silence; "resample keeps the first sample" misses a resampler that zeros everything after it.
3. Add the assertion that kills that bug, still inside `cargo test`. Do not weaken an existing test to make room.
4. Run `python3 pcmkit/oracle/mutation_smoke.py` and confirm the quantizer mutant is still killed. Your new property should not be able to turn that smoke green by accident.
5. The heavy job already runs cargo-mutants 26.0.0 on `clamp.rs` (9 caught, 2 equivalent misses). In five lines, say whether you would widen that file list. Widening belongs in the heavy workflow with the same time limit, not in `make fast`. The hand-written quantizer mutant stays in the light job either way.

## Done when

`cargo test --offline -p pcmkit --lib` passes, and you can point at the input that would fail if the bug returned. A property you cannot falsify with a small counterexample is the starter, even if the prose sounds quantified.

Module 7 asks what a sanitizer and a proof add once the tests can already fail.
