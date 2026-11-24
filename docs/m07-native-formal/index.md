# 7. Native code and light formal methods

Coming soon.

`pcmkit` crosses a boundary the Rust tests do not see: a C ABI and a C++ consumer. AddressSanitizer and UndefinedBehaviorSanitizer on that consumer, and Miri on the conversion code, are the checks that belong next to a gain function which clamps and a WAV writer which computes sizes by hand. [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html), [Miri](https://github.com/rust-lang/miri), [clang-tidy](https://clang.llvm.org/extra/clang-tidy/), and [Kani](https://model-checking.github.io/kani/) are the tools. The consumer's CMake file already has a sanitizer option, default off, so this milestone's CI stays light.

A bounded proof that gain does not overflow is worth doing once the property is the one you mean. Boris Cherny's account of the Agent SDK work used Opus 5.5, Lean, and TLA+, across 16 pull requests ([LinkedIn](https://www.linkedin.com/posts/bcherny_i-used-opus-55-to-formally-verify-the-claude-activity-7508309724598263808-TVJY)). The proof is about a model of the code. [The proof passes. Of what?](https://stravica.ai/blog/the-proof-passes-of-what/) is the question to keep on the page (read from an excerpt). A green Kani run that proves a simplified gain, while the FFI clamps with a different rule, is a pass of the model.

A performance budget belongs in the same module. A normalize that allocates per sample can pass every functional check and miss a realtime thread. [Criterion](https://bheisler.github.io/criterion.rs/book/) is the later tool. It is not in light CI.

!!! note "Codex and Cursor"

    Sanitizers and Miri are commands. Name them in `AGENTS.md` and the Cursor rule when this module lands, and do not expect either tool to run them as a hook. The C++ consumer is already the portability story: the Rust agent and the C++ caller have to share one check.

Back to the [syllabus](../syllabus.md).
