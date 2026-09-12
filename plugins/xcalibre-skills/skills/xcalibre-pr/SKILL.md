---
name: xcalibre-pr
description: Prepare and verify pull requests against XCALibre.jl project expectations. Use when checking, preparing, or submitting an XCALibre.jl pull request.
---

# XCALibre Pull Requests

Prepare a focused, current, tested pull request that follows XCALibre.jl contribution conventions.

## Checklist

1. Run `python scripts/xcalibre_pr.py preflight` from the skill directory, passing `--repository <checkout>` and `--feature` for new functionality. Supply `--description-file <path>` until an assigned pull-request number can be used to read the description from GitHub.
2. Confirm that the feature branch contains the current base branch and exactly matches its remote tracking branch. Resolve any divergence before submission.
3. Review the reported commits and changed files. Pass the single-theme check only when every change serves one coherent purpose; otherwise split the work into separate branches and pull requests.
4. Use the actual assigned pull-request number for the final changelog check. The script's `next-number` command is a prediction only because GitHub issues and pull requests share a sequence and concurrent activity can claim that number.
5. Confirm that `CHANGELOG.md` contains one or more relevant bullet items referencing `[#<number>]` or `[#<number>](@ref)`.
6. For new functionality, require relevant tests, documentation that follows the existing project convention, and a minimal example under `examples/`. Prefer an existing grid. Accept a new grid only when it is necessary and very small.
7. Require a successful local `Pkg.test()` run before submission. Exit code `0` means all automated checks passed; `1` means failure; `2` means a review or skipped test remains unresolved.
8. Confirm that the pull-request description clearly explains what was added or changed.
9. Permit docstrings only for user-level API functions. Use comments for internal implementation details and keep every comment block to no more than three lines.
10. When a dependency is added, require the pull-request description to list it and state its licence explicitly.
11. When a common or base function changes, inspect its callers and propagate the change through every affected part of the codebase, including tests and documentation.
12. Open the pull request through the human contributor's authenticated GitHub account. Never use an agent or bot identity as the pull-request author. Pass the contributor's GitHub login with `--expected-author`, then verify the assigned pull request reports that login as its author.
13. Add a short final line to the pull-request description in the form `AI assistance: <vendor>, <model>.` Pass the same values with `--ai-vendor` and `--ai-model`. Use the actual vendor and model reported by the host; do not guess. This disclosure does not make the AI an author or co-author.

Use `python scripts/xcalibre_pr.py next-number --repository <checkout>` when a provisional number is needed. Re-run preflight with `--pr-number <actual-number>` after GitHub assigns the pull-request number. Record completed semantic reviews by repeating `--confirm <review>`, using the review names reported by `--help`.

## Open items and consent

- Collect every failed, skipped, and unresolved review item into one list.
- Ask the user to implement each open item or explicitly authorise the agent to implement it. Do not amend the contribution without that consent.
- If no open item remains, continue with the submission only when submission was included in the user's request.
- Remind the contributor, as a courtesy, to confirm whether the proposed change has already been discussed with the XCALibre.jl development team.

## Implementation

- Put repeatable checks and actions in cross-platform scripts under `scripts/`.
- Prefer Python's standard library and avoid shell-specific behaviour so the same implementation runs on Linux, macOS, and Windows.
- Resolve paths from the repository root; do not rely on a particular checkout location.
- Make read-only checks the default. Perform commits, pushes, pull-request creation, or other external changes only when included in the user's request.
- Report every check as passed, failed, skipped, or requiring review. Do not treat a heuristic as proof.
