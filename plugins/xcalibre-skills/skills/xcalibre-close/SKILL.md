---
name: xcalibre-close
description: Close a phase or feature and prepare it for pull-request submission. Direct invocation only — do not select automatically; use when the user explicitly says close the phase, wrap up, tidy up before merging, archive this feature, or ships a phase's last step. Consolidates the development record, cleans shipped material, runs the close gate, and hands the result to `xcalibre-pr`; it does not commit or open the pull request.
---

# Phase / feature close

During development, `xcalibre-dev` keeps a journal so a crashed session can resume. Close is for the NEXT READER, a human with none of that context, so closing is mostly DELETION. The test for every line kept: **would someone starting fresh next month be worse off without it?** If not, git already has it.

Two things are never deleted: the shipped code, and the record of what was TRIED AND FAILED, which stops the next piece of work repeating a dead end.

Before handoff, read `../xcalibre-pr/SKILL.md`, run its preflight checks, and report any open items. Close never commits or opens the pull request; when the checks pass, tell the user to invoke `xcalibre-pr` separately for submission.

## 0. Preconditions - refuse to close on a soft floor
Working tree clean, no open question in `dev/STATUS.md`, and the FULL gate green, run cold in this session. `git ls-files dev` prints nothing (else `git rm -r --cached dev`). A close that ships a stale green is the one mistake nothing catches later. If any of these is untrue, ask the user before closing. Never close to tidy a red.

`<slug>` = the phase or feature name.

## 1. Consolidate the record → `dev/archive/<slug>/`
From `dev/STATUS.md`, `dev/journal.md` and `dev/runs.jsonl`, write:

- **`dev/archive/<slug>/README.md`** (≤ 80 lines): what was built, in plain sentences; the layout as built, naming real files; one working API snippet; what it does NOT do; and the closing SHA.
- **`dev/archive/<slug>/FAILED.md`** (≤ 40 lines): what was measured dead, one line each with the number that killed it, so the idea is recognised if it comes up again.

Then move `journal.md` and `runs.jsonl` into `dev/archive/<slug>/` and reset `dev/STATUS.md` for whatever comes next.

## 3. Examples become EXAMPLES
A test harness and an example are different artifacts, and during a build the harness wins. Invert
it: an example is read by a user who wants to know **how to drive the API**.
- Each example is a SELF-CONTAINED SCRIPT read top to bottom - build the input, configure, run,
  inspect - with the API calls visible, not behind a helper taking a case name.
- Shared machinery that deserves to stay shared (fixture inputs, a report printer, an output writer)
  goes in one support file, and it must be the boring part. Nothing showing the API's SHAPE lives
  there.
- Every example runs from the repo root with one documented command and says in two lines what it
  demonstrates and what it writes.
- The case manifest the gate iterates is a TEST concern: move it under the test tree.

## 4. Purge the comments
The build loop writes comments that argue with a reviewer; a shipped codebase has none.
**Delete outright:** every decision/requirement/step id in a comment - the reader cannot resolve
them and they rot the instant the record is renumbered; narration (what a step did, what it used to
do, what a previous attempt got wrong); CAPITALISED emphasis; any comment arguing the code is
correct; comments restating the code; banner dividers.
**Keep, one line each:** why a non-obvious choice was made, a constraint not visible locally, a unit
or convention, a known ceiling and its upgrade path.
**Docstrings** are the public contract: keep them, rewritten to say what the function takes, returns
and guarantees - not why it was built that way.

Work largest comment count first, and rewrite by LINE RANGE off a comment-block dump
(`scripts/comment_blocks.py <file> --over 3`) rather than reading whole files. A mechanical sweep for
id parentheticals is cheap and safe; read back what it leaves - stripping an id mid-sentence leaves
prose that no longer parses. After each file confirm only comments moved:
`git diff -U0 -- <file> | grep -E '^[+-]' | grep -vE '^[+-]\s*#|^[+-]{3}'`.

## 5. Delete the generated leftovers
Logs, evidence dumps, replay fixtures, probe output, meshes, screenshots, one-shot scripts whose
question is answered. KEEP only scripts that will be run again (the gate, a benchmark, a comparison
harness) - each with a one-line entry in the scripts index, and **renamed off any step id**, since
those ids are being retired. Keep reusable fixture inputs. Verify the ignore rules still cover what
the tooling regenerates.

Nothing under `dev/` goes into a project commit.

## 6. Validate packaged skills
Do not synchronise installed skill copies. If a workflow skill changed during close, confirm the
canonical copy under `plugins/xcalibre-skills/skills/` passes validation. Marketplace updates ship
after the skills repository change is committed and pushed.

## 7. Gate and hand off
- **Run the full gate again, cold.** The cleanup touched comments, examples and specs; a green
  before it is not a green after it.
- Confirm `git status --porcelain` and `git diff --name-only <base>...HEAD` list nothing under
  `dev/`.
- Run the `xcalibre-pr` preflight checks and report every open item.
- Do not commit, push, merge, or open a pull request. When the checks pass, tell the user to invoke
  `xcalibre-pr` separately to commit and open the pull request.

## Close report
Verdict first, then: the gate result, what `dev/archive/<slug>/` contains, the counts (files deleted,
comment lines removed, examples rewritten), anything deliberately kept that looked deletable, and
the pull-request preflight result and remaining open items. No essay.
