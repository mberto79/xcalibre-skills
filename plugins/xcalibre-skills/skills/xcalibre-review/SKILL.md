---
name: xcalibre-review
description: Review an XCALibre.jl pull request, branch or diff — PR rules, fit with the existing API and architecture, CPU/GPU/MPI coverage, performance and allocations, and correctness — with required changes posted inline from the account holder's GitHub account. Use when the user asks to review XCALibre.jl changes ("review this PR").
---

# XCALibre Review

Review of an XCALibre.jl contribution, posted by the account holder. When the user asks for a review, take the PR, branch or working diff they name and run the three steps below in order. A maintainer performs the final review and merge.

## 1. PR rules

Run `python ../xcalibre-pr/scripts/xcalibre_pr.py preflight` against the target, with the same arguments `xcalibre-pr` uses. If the changes do not serve one purpose, stop and propose a split into one PR per theme instead of reviewing the code. Otherwise carry every FAIL and REVIEW item into the report as open items.

## 2. Code review

Read the changed code against the surrounding XCALibre.jl source, and check the source whenever a claim needs it. Look for:

- **Architecture.** The change follows how XCALibre.jl is built: behaviour selected by dispatch on types, not runtime flags; models and configuration in the existing structs; mesh and field types kept type-stable ([xcalibre-mesh-types](../xcalibre-mesh-types/SKILL.md)); backend-independent loops through `KernelAbstractions.jl` ([xcalibre-kernels](../xcalibre-kernels/SKILL.md)); existing utilities reused rather than duplicated. A parallel code path left with the old behaviour (another solver, equation or solve path) is a finding.
- **Every backend.** The change must work on CPU, on GPU through `KernelAbstractions.jl`, and on MPI-distributed meshes, including halo exchanges. Code that only works on one, or that silently falls back to a serial CPU path, is a finding.
- **Performance and allocations.** XCALibre.jl is a CFD solver, so performance is protected, and allocation is expensive on GPU. Flag any allocation inside the solver iteration, and in per-cell or per-face paths; type instability and abstract containers; temporary arrays from broadcasts, slices or `collect`; work that can be hoisted out of a loop or fused into an existing kernel; extra kernel launches or host–device transfers; scalar indexing or serial loops that block the GPU. Also name clear opportunities to cut allocations or time in the code the change touches, marked as opportunities, not defects. When a claim is uncertain, measure it ([julia-benchmarking](../julia-benchmarking/SKILL.md)).
- **Correctness.** Obvious bugs and unhandled edge cases.

Verify each candidate against the code and mark it CONFIRMED or PLAUSIBLE. Report only what survives, most severe first; an empty list is a valid result. Prefer a few high-signal findings to nits, and do not modify files unless `--fix` was requested.

## 3. Post the review

Put each required change inline, on the exact lines it concerns, with one or two sentences on what to change and why. Add one short summary review: the verdict, the open preflight items, and a final line `AI assistance: <vendor>, <model>.` using the vendor and model the host reports.

Every comment and review is posted through the account holder's own authenticated GitHub account, for example with `gh api` as the signed-in user. Before posting, check that `gh api user` returns a personal account, not a bot or app identity; if it does not, stop and show the review in the session instead. Never post as an AI, bot or app account, and never sign a comment as the AI. Show the review to the user and post it only once they confirm.

For a local diff with no pull request, give the same review in the session, with each change located as `file:line`.

## Interface

```text
xcalibre-review [target] [level] [--fix]
```

- `target`: omit for the working diff, or pass a PR number, branch or path.
- `level`: `low`/`medium` for fewer, high-confidence findings; `high`/`max` for broader coverage.
- `--fix`: apply the required changes to the working tree, only when the user asked for it.

Never post, push or modify files without the user's confirmation.
