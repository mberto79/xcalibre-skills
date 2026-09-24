# Opening a feature vault

Read this when running `init --feature <slug> [--branch <name>]`, or when writing or closing a feature's own records. Everything else in `SKILL.md` applies inside a feature vault unchanged.

## Contents
- What a feature vault is and where it lives
- Several features at once: one branch, one feature
- The five steps, in order, before any milestone exists
- Proportionality: how much ceremony a feature earns
- How a feature vault closes

## What a feature vault is

`init --feature <slug>` creates the feature's vault at `dev/features/<slug>/`, beside the project's own, scaffolding the project vault first when there is none - so a feature is how a project acquires one. Every record, budget, ID rule and check applies inside it unchanged; `check` reads every vault in the repository and names the one each error is in. A vault a previous version of this skill opened AS `dev/` is grandfathered, not moved.

## Several features at once

A feature is built on ONE project branch, and `dev/features/INDEX.md` records which: ``- [ ] <slug> on `<branch>` - <what it delivers>``, written by `init` from the checked-out branch or `--branch`. The index is the home of that binding; the feature's `activeContext.md` `BRANCH:` is its per-write snapshot. Because `dev/` is excluded from the project, it survives a branch switch, and `resume` and `plan` follow the switch to the bound feature without `--feature`. Open the feature on its branch, not on the base branch, or the base branch is bound to it. A branch holds one open feature; two features on one branch are one feature or two branches. Work that belongs to no feature stays in the project vault.

THE VAULT IS THE FEATURE'S, AND SO IS ITS SPEC. Its `spec.md` states what THE FEATURE must be true of when delivered - never the host project's requirements restated - and names the project's requirement IDs, or the existing code's behaviour, as INHERITED CONSTRAINTS it may not break. `roadmap.md` and `phaseRoadmap.md` are the feature's technical roadmap, not the project's.

The records are not filled in from the request alone. In this order, each step owed before the next means anything:

1. **The request, verbatim.** What the user asked for, in their terms, recorded before interpretation, so anything the requirements add is visibly an interpretation.
2. **The host survey**, written into the feature's `architecture.md` BEFORE any requirement or milestone exists. Read the code, not its documentation: the entry points the behaviour will be reached from, the components it touches and what each owns today, the interfaces other code depends on and how each is verified, and the conventions the surrounding code actually follows. With no code yet, this section says so in one line.
3. **The attachment.** Where the feature joins the existing shape, why there rather than the alternatives, and what would have to change if that choice proves wrong - the cost of the choice, stated before it is taken.
4. **The feature's spec** - outcomes, acceptance, inherited constraints. NOTHING IS INVENTED: a requirement the user did not state and the codebase does not imply is an OPEN QUESTION with what it blocks and who settles it, never an invented requirement. A question whose answer changes the shape of the work is asked before that work starts.
5. **The roadmap and milestones** - the technical route to that spec, under the ID rules. A small feature is one phase of a few milestones, no more.

THE CEREMONY IS PROPORTIONAL TO THE FEATURE, AND ALL FIVE STEPS ARE STILL OWED. A step whose honest answer is short is WRITTEN short: a self-contained addition's host survey and attachment are a line each; a day's feature gets one phase and two milestones, not a roadmap. The ORDER is never skipped - request before interpretation, code before plan, the attachment's cost before it is taken - because that order stops a vault recording an invention as a requirement. A vault whose scaffolding costs more than its feature has failed its purpose.

A feature vault closes as a phase closes: its records move to its own `archive/`, and what the host project must keep - a requirement the feature added to the product, a trap worth carrying, a decision the project will be asked about again - is COPIED into the project's vault with a decision recording the move. A vault left behind after the feature ships is history, and goes to `archive/`. Its index row is closed in the same act - `[x]` with the archive path, or `[-]` naming where the work went - which frees the branch; the row itself is never deleted.
