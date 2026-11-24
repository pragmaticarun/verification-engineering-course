# Project 3. Make a second directory agree

About ninety minutes. You finish with a copy of the harness that the auditor accepts, and one deliberate break you can explain.

## Do this

1. Copy `harness/` to `/tmp/pcm-rules`. Do not edit the course copy.
2. Run `python3 labs/m03/solutions/audit.py /tmp/pcm-rules` and confirm it prints `ok`.
3. Add one rule you actually want for audio work, in all four instruction files. Example: "a gain that is not finite must leave the buffer unchanged." Keep `AGENTS.md` well under 32 KiB.
4. Break one copy on purpose. Remove the done sentence from the Cursor rule only. Re-run the auditor and read the line it prints.
5. Restore the sentence. In `settings.json`, add a deny you can justify, such as a read of a local recordings directory, using the same `Read(...)` shape as `.env`. Re-run the auditor. It checks that `.verify` and `.claude` are still covered. It will not notice a typo in your new pattern, so read the JSON yourself.

## Done when

The auditor prints `ok` on the repaired copy, you have seen it fail on a one-file edit, and you can say which tool would have ignored the rule if you had written it only in `CLAUDE.md`.

Leave `harness/` as CI audits it. Module 4 wires the Stop and PreToolUse commands that this module only checks are registered.
