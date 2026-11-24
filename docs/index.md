# Verification engineering for AI coding agents

You can already ship C++, Rust, and Python. The new problem is not typing the function. The new problem is knowing the function is the one you asked for when a coding agent typed it, and when several agents typed several of them before lunch.

This course is that skill, practiced on one small audio library. A check either exits 0 or it does not. Everything else — a confident summary, a ticked box, a file called `evidence.md` — is a claim.

## Who it is for

Arunkumar, this is built for the way you already work: Ubuntu, Rust and C++ in the same tree, Python when you want a reference implementation, and media signals that have real invariants. Peak is either 1 or it is not. Silence is either finite or it is NaN. A C ABI either clamps or it writes past full scale and the C++ consumer hears it.

You do not need to be new to agents. You need a harness you can test without an API key.

## What you will be able to do

Design a verification harness, run it on recorded agent sessions, and read one evidence file instead of every diff. The harness in this repository is an improved design, not a transcript of someone else's files. Where a popular write-up is loose, the lab shows the loose version accepting a cheat and the corrected version rejecting it.

## This milestone

Modules 1–12 and the capstone are the full lessons. The measurements are fixtures. No module calls a model.

| Piece | Where |
| --- | --- |
| Why a green tick is not a result | [Module 1](m01-why-verification/index.md) |
| Briefs, non-goals, allowed files, acceptance commands | [Module 2](m02-defining-done/index.md) |
| `CLAUDE.md`, `AGENTS.md`, Cursor rules, deny rules | [Module 3](m03-instructions-permissions/index.md) |
| Stop and commit gates, tested on recorded events | [Module 4](m04-hooks-gates/index.md) |
| Formatters, linters, goldens, and the C ABI, in one fast tier | [Module 5](m05-fast-layers/index.md) |
| Properties, a differential oracle, a fuzz smoke, one mutant | [Module 6](m06-cant-fool-tests/index.md) |
| Sanitizers, one Miri test, and what a proof is about | [Module 7](m07-native-formal/index.md) |
| An end-to-end `pcmx` run whose notes say what was not checked | [Module 8](m08-run-and-prove/index.md) |
| Held-out cases, a tamper scan, and a ruleset that is still a template | [Module 9](m09-reward-hacking/index.md) |
| One rubric reviewer, scored on a report split | [Module 10](m10-agents-verifying-agents/index.md) |
| Six worktrees and a budget of eight | [Module 11](m11-orchestration/index.md) |
| Reads per ship, escapes, and a pruner that keeps a quiet lock | [Module 12](m12-metrics-ratchet/index.md) |
| The same eight changes, before the harness and after it | [Capstone](capstone/index.md) |
| The running example | `pcmkit/` |
| The harness you can copy | `harness/` |

Each module is about four hours: a short reading, a lab with tests, a quiz, and a project that leaves something behind in `pcmkit` or the harness.

## How the teaching works

The opening of each module is the idea, then a failure you can picture in `pcmkit`, then a diagram. The code blocks are not pasted. They are included from files CI runs. If a snippet and the test disagree, the build is wrong, not the prose.

Exercises hide the solution in a collapsible note. The starter programs in `labs/` fail the exercise on purpose. The programs in `labs/*/solutions/` pass. CI checks both.

## Two licences

Prose is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code is [MIT](https://opensource.org/licenses/MIT). See `LICENSE` and `LICENSE-CONTENT`.

## Where the ideas come from

A public X article by @0xarcos, "Verification Engineering: The $400K Skill of Running 30 Fable 5.2 Agents", posted 18 November 2026, is the spark. The durable part of that article tracks Addy Osmani's note on how the Claude Code team thinks about verification, and the Claude Code docs for hooks, skills, and permissions. The file-by-file harness in the article is the author's reconstruction. It has holes. We keep the question it asks and we close the holes.

Read the [claim check](claims.md) before you treat a number in that article as a measurement, and the [map](mapping.md) if you want to see which section became which module.

Primary sources are listed on the [references](references.md) page. Nothing here asks you to paste an API key into CI.
