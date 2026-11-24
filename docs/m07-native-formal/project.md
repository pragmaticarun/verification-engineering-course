# Project 7. Label the check you actually have

About ninety minutes. You finish with a sanitizer run you can describe accurately, and one sentence a reviewer cannot misunderstand.

## Do this

1. Run `bash pcmkit/cpp/run_sanitizers.sh`. Confirm the consumer prints `ok`.
2. Write six lines a reviewer can check against the script:
    - which compiler built the C++ file
    - which sanitizers were linked
    - whether the Rust library was instrumented
    - which functions the consumer called
    - one bug the run would not see
    - the command, so the claim is replayable
3. Run the i16 grid test by name and time it. Put the time in the note. If you describe it as exhaustive, say exhaustive over what.
4. Optional, only if you already have the pinned nightly: run the Miri command from the lab. If you do not, write "Miri not run locally" and point at the heavy workflow. Do not infer a local result from the existence of the workflow file.

## Done when

A reader who has not taken the module can tell the sanitizer binary from a Kani proof and from the i16 grid. If your note uses the word "proved," the next sentence should say of what, on which inputs, by which command.

Module 8 takes the commands you trust and puts their stdout into an evidence file a person can read without replaying your afternoon.
