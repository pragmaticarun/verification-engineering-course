# 12. Metrics and the ratchet

Coming soon.

Module 1 computes reads per ship from a fixture. This module computes it from trailers and from CI, and adds the numbers a fixture cannot show: escapes that reached `main`, cost, latency, false blocks, and the catch rate on the corpus. A miss becomes a check. That loop is the one the [verification note](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) describes, including the path where three agents try to disprove a proposed rule before a person adds it.

The article also says to prune every check that has not fired in 60 days. The note says the list is tidied on a routine. Sixty days is the author's number. A check for a rare, expensive failure can be quiet for longer than that and still be the one you wanted. The later report will weight a check by the incident it exists for, and it will not delete a check only because it has been silent.

The capstone uses these numbers. A before and after that is a checklist you once followed is not a result. A before and after that is reads per ship, catch rate, and escapes, on the same corpus, is.

!!! note "Codex and Cursor"

    Metrics come from git and from the workflow logs. They are tool-agnostic on purpose. An instruction file that says "ship faster" will move the numbers in the wrong direction. The files should keep pointing at the runner.

Back to the [syllabus](../syllabus.md).
