# Opening a feature vault

Read this when `init --feature <slug>` is run, or when a feature's own records are being written or closed. Everything else in `SKILL.md` applies inside a feature vault unchanged.

## Contents
- What a feature vault is and where it lives
- The five steps, in order, before any milestone exists
- Proportionality: how much ceremony a feature earns
- How a feature vault closes

## What a feature vault is

`init --feature <slug>` creates a vault for that feature. It is placed at `dev/features/<slug>/` beside the project's own, and IS `dev/` when the project has no vault yet — so a feature is how a project acquires one. Every record, budget, ID rule and check above applies inside it unchanged; `check`, `resume` and `plan` take `--feature <slug>`, and `check` with no flag reads every vault in the repository and says which one an error is in.

THE VAULT IS THE FEATURE'S, AND SO IS ITS SPEC. `spec.md` there states what THE FEATURE must be true of when it is delivered — never the host project's requirements restated. It names the project's own requirement IDs, or the behaviour of the existing code, as INHERITED CONSTRAINTS it may not break. `roadmap.md` and `phaseRoadmap.md` are the technical roadmap for building the feature, not the project's.

The records are not filled in from the request alone. In this order, and each step is owed before the next means anything:

1. **The request, verbatim.** What the user asked for, in their terms, recorded before it is interpreted, so that everything the requirements add to it is visibly an interpretation.
2. **The host survey**, written into the feature's `architecture.md` BEFORE any requirement or milestone exists. Read the code, not its documentation: the entry points the behaviour will be reached from, the components it touches and what each owns today, the interfaces other code depends on and how each is verified, and the conventions the surrounding code actually follows. For a project with no code yet this section says so in one line.
3. **The attachment.** Where the feature joins the existing shape, why there rather than the alternatives, and what would have to change if that choice turns out wrong. That last is the cost of the choice and is stated before it is taken.
4. **The feature's spec** — outcomes, acceptance, inherited constraints. NOTHING IS INVENTED: a requirement the user did not state and the codebase does not imply is an OPEN QUESTION with what it blocks and who settles it, never a requirement written on their behalf. A question whose answer changes the shape of the work is asked before that work starts.
5. **The roadmap and milestones** — the technical route to that spec, under the ID rules above. A small feature is one phase of a few milestones; it does not need more.

THE CEREMONY IS PROPORTIONAL TO THE FEATURE, AND ALL FIVE STEPS ARE STILL OWED. A step whose honest answer is short is WRITTEN short: a self-contained addition's host survey and attachment are a line each, and a feature that will take a day gets one phase and two milestones, not a roadmap. What is never skipped is the ORDER — the request before its interpretation, the code before the plan, the cost of the attachment before it is taken — because that order is what stops a vault recording an invention as a requirement. A vault whose scaffolding costs more than the feature it carries has failed its own purpose.

A feature vault closes as a phase closes: its records move to its own `archive/`, and what the host project must keep — a requirement the feature added to the product, a trap worth carrying, a decision the project will be asked about again — is COPIED into the project's vault with a decision that says it moved. A vault left behind after the feature ships is history, and history goes to `archive/`.
