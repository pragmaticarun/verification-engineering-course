# Quiz 6

### 1

Why does the toward-zero mutant survive the starter?

??? success "Answer"

    The starter only checks `-1`, `0`, and `1`. Those three codes match the rounding quantizer. `0.2` does not, and the starter never asks.

### 2

What does `mutation_smoke.py` prove, and what does it not prove?

??? success "Answer"

    It proves this suite can kill this one hand-written mutant, and that a weaker property cannot. It does not produce a mutation score, and it does not run cargo-mutants. The heavy job runs cargo-mutants 26.0.0 on `clamp.rs` only: 9 caught, 2 equivalent misses. mutmut is still not installed.

### 3

Why is the property generator a fixed seed instead of proptest?

??? success "Answer"

    So the light job stays deterministic and dependency-free. A failure repeats. Proptest is the library you would add, pin, and cache if you wanted shrinking. It is cited and not installed.

### 4

The parser smoke passes. Are you fuzzing?

??? success "Answer"

    You are running a fixed smoke that forbids panics on those inputs. The heavy job also runs cargo-fuzz 0.13.2 on `wav_parser` for 15 seconds. That is a time box. The light-job test is still the fixed sequence. Call each run what it is.

### 5

ImpossibleBench's read-only tests stop one cheat. Which cheats remain?

??? success "Answer"

    Special-casing on the test name, and operator overloading. The paper also describes state recording. Hiding the tests drives cheating down and also hurts legitimate passes. Read-only is a middle ground, not a lock.

### 6

Two implementations agree. Is the behavior right?

??? success "Answer"

    Not yet. They can share a bug. Agreement is a fact that the two sides match. The brief, from module 2, is what says the match is the behavior you wanted.
