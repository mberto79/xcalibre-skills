# P1-M1 — <milestone title> (plan)

Linked from `dev/phaseRoadmap.md`. Requirements: <IDs from `dev/spec.md`>. Governing decisions: <D ids>.

## Problem, quantified

What is wrong, measured. Numbers with their instrument, not adjectives.

## Approach

What will be built and why this shape rather than the alternatives. Mechanism detail that outlives the milestone belongs in `dev/architecture.md` once it lands.

## Configuration space

The local configurations this milestone must hold on, as a product of named parameters, and the generated catalogue that covers it (`dev/scripts/`); the gate is that table, never one hand-built case.

## Steps

Steps are `P1-M1-S<j>`, allocated in order and never renumbered. Same state markers as a milestone: a step closed without delivering keeps its line and names where the work went. Each row states its mechanism, its cost and its verdict BEFORE it is built.

- [ ] **P1-M1-S1** <what it changes> — mechanism: <the invariant it follows from> — cost: <per unit of work> — verdict: <what would accept or refuse it>.
- [ ] **P1-M1-S2** <what it changes> — mechanism: <...> — cost: <...> — verdict: <...>.

## Exit criterion

What must be true for the milestone to close. On close this file moves under the same name to `dev/archive/plans/<phase>/`; its reviews go to `dev/archive/reviews/<phase>/`.

## Open questions

Questions whose answer changes the approach, each with who or what settles it.
