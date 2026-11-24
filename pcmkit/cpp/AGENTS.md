# C++ consumer

Done is a claim: a command exited 0 on this tree.

When the change is under `pcmkit/cpp/` or `pcmkit/include/`, the command is `bash pcmkit/cpp/run_consumer.sh`. ASan and UBSan stay off unless the build explicitly passes `-DPCM_SANITIZERS=ON`. Do not paper over an FFI failure by catching it in `main` and returning 0.
