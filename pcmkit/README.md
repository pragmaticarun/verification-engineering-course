# pcmkit

A small WAV/PCM library, a `pcmx` CLI, a C ABI with a C++ consumer, and a Python reference. It is the running example for the verification-engineering course.

This milestone covers parse/write (16-bit, 24-bit, float), gain with clamping, peak normalize, mix, linear resample, peak/RMS, and a grayscale waveform PNG. Fuzz targets, sanitizer CI, and mutation runs are later modules. The CMake sanitizer switch is present and off by default.

```bash
cargo test --manifest-path pcmkit/Cargo.toml --offline
python3 pcmkit/oracle/test_oracle.py
bash pcmkit/cpp/run_consumer.sh
```
