# Quiz 7

### 1

The starter accepts `broken`. Why?

??? success "Answer"

    `broken(0.5)` returns 1, and that is the only input the starter uses. The other codes overflow the range, and the starter never calls them.

### 2

Name the four objects in "the proof passed," following Barry's split.

??? success "Answer"

    The code, the model of the code, the property, and the requirement. A proof connects the model and the property. The other two ends are a separate argument.

### 3

What does the sanitizer script instrument?

??? success "Answer"

    The C++ consumer, with AddressSanitizer and UndefinedBehaviorSanitizer. The Rust static library is the stable, uninstrumented build. The script is not a sanitizer run of the Rust gain loop.

### 4

Why is Miri on a nightly toolchain instead of Rust 1.83.0?

??? success "Answer"

    The 1.83.0 channel does not offer a Miri component for this target. The heavy job pins `nightly-2026-11-23` and runs one test. The light job stays on 1.83.0.

### 5

The normalize tripwire allows two seconds. What regression will it miss?

??? success "Answer"

    A small one. It is a tripwire for a huge slowdown, not a Criterion benchmark. Criterion is cited and not run.

### 6

The diagram has both the i16 grid and a Kani harness. What do you write in the pull request?

??? success "Answer"

    If you mean the grid, name `every_i16_code_stays_in_range_at_the_gain_grid`: every i16 code at five gains, in `apply_gain_db`. That test is not a Kani proof. If you mean Kani, name `clamp_unit_holds_an_i8_grid`: every i8 divided by 16, through `clamp_unit`, stays inside [-1, 1]. You do not write that one of them proved the other.
