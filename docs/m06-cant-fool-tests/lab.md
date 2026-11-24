# Lab 6. Kill one mutant

The starter property asks for the codes of `-1`, `0`, and `1`. The toward-zero quantizer matches those three and misses `0.2`. The solution compares the longer sample list to the rounding quantizer.

```python
--8<-- "labs/m06/starter/property.py"
```

```python
--8<-- "labs/m06/solutions/property.py"
```

```text
python3 labs/m06/starter/property.py mutant
python3 labs/m06/solutions/property.py mutant
python3 labs/m06/solutions/property.py correct
```

The starter exits 0 on `mutant`. The solution exits 1. On `correct`, the solution exits 0. CI asserts that split. The same split, against the oracle's own quantizer, is `python3 pcmkit/oracle/mutation_smoke.py`.

## The properties cargo actually runs

In `pcmkit/crates/pcmkit/src/course_checks.rs`, three tests are this module's fast half:

- `i16_encoding_is_idempotent_on_a_fixed_seed` encodes, parses, and encodes again.
- `normalize_is_idempotent_on_a_fixed_seed` normalizes twice, and checks that silence stays at peak 0 while anything else lands on peak 1.
- `parser_does_not_panic_on_a_fixed_fuzz_smoke` mutates a valid WAV and also feeds short random buffers.

They use a fixed xorshift seed. A failure prints the same inputs tomorrow. That is the point of keeping proptest out of the light job: shrinking is valuable, and a non-reproducible failure in CI is a flake, which module 5 just banned.

Run them:

```text
cargo test --manifest-path pcmkit/Cargo.toml --offline -p pcmkit --lib i16_encoding
cargo test --manifest-path pcmkit/Cargo.toml --offline -p pcmkit --lib normalize_is_idempotent
cargo test --manifest-path pcmkit/Cargo.toml --offline -p pcmkit --lib parser_does_not_panic
```

Then the oracle, which is the differential check:

```text
python3 pcmkit/oracle/test_oracle.py
```

## Walk through a disagreement

Change `quantize_i16` in `pcmkit/oracle/reference.py` to truncate, run `mutation_smoke.py`, and watch the differential side fail. Put the rounding back before you commit. The smoke is there so you do not have to keep a broken quantizer in the tree to believe the story. The lab's `quant.py` is the copy you are allowed to mutate in an exercise, because CI's solution compares it to itself.

## Exercise

You want a property for `normalize_peak`: "the peak is at most 1."

??? success "What input shows that this property is too weak?"

    Any buffer that the function returns unchanged, including a quiet one. The peak is already at most 1, so a no-op passes. The property you want also says: if the buffer was not silence, the peak is 1, and normalizing again changes nothing. That is the test named `normalize_is_idempotent_on_a_fixed_seed`. "At most 1" is the clamp. It is not the normalize.

## Exercise

The fuzz smoke has passed for weeks. A sample you recorded in the field makes `parse_wav` panic.

??? success "What do you add, and what do you not claim?"

    Add the bytes, or a reduced version of them, to the smoke or to a unit test, so the panic stays dead on the light job. The fixed sequence was not coverage-guided. The heavy job's 15-second `wav_parser` run is a search, and it can miss the same bytes. A crash you care about belongs in a unit test either way.
