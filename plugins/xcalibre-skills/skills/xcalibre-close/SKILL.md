---
name: xcalibre-close
description: Close a phase or feature and prepare it for pull-request submission. Direct invocation only — do not select automatically; use when the user explicitly says close the phase, wrap up, tidy up before merging, archive this feature, or ships a phase's last step. Consolidates the development record, cleans shipped material, runs the close gate, and hands the result to `xcalibre-pr`; it does not commit or open the pull request.
---

# Phase / feature close

`xcalibre-dev` owns the build loop and optimises for RECOVERY: every dead end, decision id and probe
survives so a crashed session resumes. Close optimises for the NEXT READER, a human with none of
that context. Closing is therefore mostly DELETION; the test for every line kept: **would someone starting fresh next month be worse off without it?** If not, git already has it.

Two things are never deleted: the shipped code, and the record of what was TRIED AND FAILED - the
only artifact that stops the next phase repeating a dead end.

Before handoff, read `../xcalibre-pr/SKILL.md`, run its preflight checks, and report any open items. Close never commits or opens the pull request; when the checks pass, tell the user to invoke `xcalibre-pr` separately for submission.

**Phase close** (one phase ends, the project continues) and **feature close** (development stops)
run the same steps.

## 0. Preconditions - refuse to close on a soft floor
Working tree clean, `STATE: IDLE`, no open item in `dev/phaseRoadmap.md`, no `## blocked`, and the
FULL gate green, run cold in this session. The vault is not part of the project branch: `git ls-files dev`
prints nothing (else `git rm -r --cached dev`) and `/dev/` is in `.git/info/exclude`. A close that ships a stale green is the one mistake
nothing catches later. If any of these is untrue, ask the user before closing. Never close a phase
to tidy a red.

`<slug>` = the phase (`phase1`) or feature name. Closed records land in
`dev/archive/phases/<slug>/`.

## 1. Consolidate the record → `dev/archive/phases/<slug>/`
Move `dev/phaseRoadmap.md` to `dev/archive/phases/<slug>/roadmap.md`. From it, its reviews,
`decisions.md`, and `activeContext.md`, write:

- **`dev/archive/phases/<slug>/README.md`** (≤ 120 lines) - the entry point, for someone who has never seen the
  project: `## what it does` (plain sentences, no ids), `## architecture` (the layout AS BUILT,
  naming real files), `## the API` (one working snippet), `## what it does NOT do` (honest limits,
  so they are not rediscovered as bugs), `## record` (pointers below + the closing sha).
- **`dev/archive/phases/<slug>/decisions.md`** - the decisions that ARE the shipped design, renumbered
  `<slug>-01` upward in the order a reader needs them, one line each:
  `- <slug>-NN <what was decided> - why: <reason>`. A superseded decision is not a shipped decision.
  Renumbering is the point: the next phase starts at D1 with no collision.
- **`dev/archive/phases/<slug>/FAILED.md`** (≤ 60 lines) - what was measured DEAD, one line each with the number
  that killed it and enough detail to recognise the idea if it is proposed again. A dead end needs
  its epitaph, not its biography.

Then delete superseded loose plan fragments, answered probes, and the phase's project-level
`decisions.md` block. Existing historical reviews stay read-only under `dev/archive/`; do not
duplicate their content in the closed phase record.

## 2. Update what SURVIVES the phase
Three project-level files are not phase records and must be brought CURRENT, never deleted:

- **`dev/architecture.md`** - the project-wide architecture as it stands today, across all phases.
  Fold in what this phase changed; drop what it retired. It is the map a rework of the main plan
  starts from; `dev/archive/phases/<slug>/README.md` is history.
- **`dev/roadmap.md`** - tick the phase with its one-line delivered result and point at
  `dev/archive/phases/<slug>/README.md`. The phase is a STEP in this plan, never the plan. Surviving `## carried`
  lines move to `## flagged`, tagged by origin phase.
- **`dev/spec.md`** - rewrite to describe the DELIVERED system: every requirement still binding, in
  plain language, without the narration of how it got that way. A requirement whose only
  remaining content is the history of its own amendments is a
  `dev/archive/phases/<slug>/decisions.md` line, not a
  requirement. Keep the vocabulary section in full - it is the most valuable thing in the file.

Then reset `dev/activeContext.md` for the next phase: `## doing` cleared, `## blocked` and `## attempts`
gone, `LOAD:` pointing at the new state. Reset `dev/phaseRoadmap.md` for the next phase, or make it
state that no phase is active when development has closed.

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
(`xcalibre-dev/scripts/comment_blocks.py`) rather than reading whole files. A mechanical sweep for
id parentheticals is cheap and safe; read back what it leaves - stripping an id mid-sentence leaves
prose that no longer parses. After each file confirm only comments moved:
`git diff -U0 -- <file> | grep -E '^[+-]' | grep -vE '^[+-]\s*#|^[+-]{3}'`.

## 5. Delete the generated leftovers
Logs, evidence dumps, replay fixtures, probe output, meshes, screenshots, one-shot scripts whose
question is answered. KEEP only scripts that will be run again (the gate, a benchmark, a comparison
harness) - each with a one-line entry in the scripts index, and **renamed off any step id**, since
those ids are being retired. Keep reusable fixture inputs. Verify the ignore rules still cover what
the tooling regenerates.

Everything this close writes under `dev/`, `dev/archive/` included, is recorded with
`xcalibre-dev sync`, never in a project commit.

Recorded numbers keyed by step id are worthless after a close - step namespaces collide across plan
revisions. Rewrite `dev/telemetry/benchmarks.csv` from the closing gate, keyed by what each number measures.

## 6. Validate packaged skills
Do not synchronise installed skill copies. If a workflow skill changed during close, confirm the
canonical copy under `plugins/xcalibre-skills/skills/` passes validation. Marketplace updates ship
after the skills repository change is committed and pushed.

## 7. Gate and hand off
- **Run the full gate again, cold.** The cleanup touched comments, examples and specs; a green
  before it is not a green after it.
- Confirm `git status --porcelain` and `git diff --name-only <base>...HEAD` list nothing under
  `dev/`, then run `xcalibre-dev sync -m "Close <slug>"`.
- Run the `xcalibre-pr` preflight checks and report every open item.
- Do not commit, push, merge, or open a pull request. When the checks pass, tell the user to invoke
  `xcalibre-pr` separately to commit and open the pull request.

## Close report
Verdict first, then: the gate result, what `dev/archive/phases/<slug>/` contains, the counts (files deleted,
comment lines removed, examples rewritten), anything deliberately kept that looked deletable, and
the pull-request preflight result and remaining open items. No essay.
