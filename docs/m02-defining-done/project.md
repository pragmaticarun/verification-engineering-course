# Project 2. A brief for one pcmkit behaviour

About two hours. You finish with a brief that the solution linter accepts and a command that fails for a reason you can point at.

## Pick one

- `pcmx info` prints `channels`, `rate`, and `format` for a 16-bit stereo WAV, and exits non-zero on a truncated header.
- `pcmx gain --db` leaves the buffer untouched when the gain is not finite, and clamps to the range the library already documents.
- The C++ consumer still prints `ok` after a gain of -3 dB. The non-goal is "no new FFI function."

## Do this

1. Write the brief under `/tmp` or in a private branch. Use the four sections from the normalize brief. Allowed files must be real paths.
2. Put a command in the acceptance section that exists. If you need a new script, write it, and keep the first version honest: it should fail on today's bug or pass on today's behaviour, and you should know which.
3. Run:

    ```text
    python3 labs/m02/solutions/brief_lint.py /tmp/BRIEF.md
    ```

4. Run the starter on the same file and notice that it cannot tell your brief from the vague one, as long as the title is present.
5. In five lines, say what you refused in Non-goals, and which `pcmkit` test already covers a neighbouring behaviour so you do not retest it by accident.

## Done when

The solution linter prints `ok`, the command runs, and you can say what exit status you required. Do not weaken `briefs/gain-normalize/BRIEF.md`. CI lints that file and runs its command.

Module 3 takes the sentence "stay inside the brief" and puts it where each tool will read it, with permissions that stop the tool from editing the sentence.
