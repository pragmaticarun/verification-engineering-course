# Project 5. One more golden, one honest timing note

About ninety minutes. You finish with a golden you generated and a sentence about how long `make fast` took on your machine.

## Do this

1. Run `make fast` once the pinned tools are installed (`requirements-checks.txt`, plus `clang-tidy`). Write down the wall time. If the first run is dominated by compiling, run it again and write down the warm time too.
2. Add a second committed golden for a buffer you choose, using the same compare-the-bytes pattern as `golden_wav_and_png_match_committed_bytes`. Keep the buffer deterministic. No clock, no temp path inside the bytes.
3. Regenerate with `UPDATE_GOLDEN=1`, then run the test again without the variable. Read the diff before you keep it.
4. Point `pcmkit/fast/flaky_scan.py` at `labs/m05/fixtures/sleepy.py` and confirm it fails. Point it at `pcmkit` and confirm it passes.
5. In five lines, say what you would move out of `make fast` if the warm run crossed a minute, and why the C++ consumer stays in even if it is the slow step.

## Done when

`cargo test` passes without `UPDATE_GOLDEN`, the scanner still rejects the sleep fixture, and your note separates a cold compile from the suite itself. Do not add insta or nextest unless you are also ready to pin them, cache them, and make CI run them. A dependency that only your laptop has is not part of the tier.

Module 6 keeps this tier and asks a harder question: can the tests fail when the code is wrong?
