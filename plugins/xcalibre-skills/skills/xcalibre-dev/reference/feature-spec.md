# <feature> - requirements

WHAT THIS FEATURE MUST BE TRUE OF WHEN IT IS DELIVERED. This spec is the FEATURE'S, never the host project's: it states what the feature must do and hold, inheriting the project's requirements rather than restating them. Where the host has a vault, name the `dev/spec.md` requirement IDs that constrain this work; otherwise name the existing code's behaviour the feature may not break.

One test admits a clause here: could a completely different implementation of this feature satisfy it? If not, it is not a requirement. How it is built is `architecture.md`; how to work on it is `gotchas.md`; why a mechanism was chosen or refused is `decisions.md`. IDs are permanent - text is amended under its existing ID and repeals are recorded in place.

## what the user asked for

The request in the user's own terms, in a few lines, before interpretation. Anything the requirements below add is an INTERPRETATION and says so.

## goal

What the feature is for, and the one property that outranks convenience when they conflict.

## vocabulary

- **<term>** - a term this feature introduces, or one the host project uses differently here.

## priority

What outranks what when two of this feature's own clauses conflict, and what the host project's priority order already imposes on it.

## quality bars

- **Q1 <name>** - the property and its numeric bar, where this feature adds one. A feature that adds none says so in one line and inherits the project's.

## requirements

One line each where possible, four at most:

`<ID> <WHAT IT ENFORCES, IN CAPITALS> - <what must be true, briefly>.`

The capitalised clause is what the requirement enforces, so the list can be scanned. The statement is an OUTCOME: it never names a keyword, function, file, constant or stage order - that is documentation, not a requirement. Anything needing more than four lines is architecture, method or a decision, and goes to those records.

A requirement the user did not state and the codebase does not imply is an OPEN QUESTION below, never an invented requirement. Nothing here is frozen: a clause is amended under its own ID, with a decision, when the work shows it should be.

F1 <WHAT IT ENFORCES> - <what must be true of the delivered feature>.
F2 <WHAT IT ENFORCES> - <...>.

## inherited constraints

What the host project already requires that this feature must not break, by ID where the project has IDs, otherwise by name.

- <project requirement ID or behaviour> - <how this feature satisfies it>.

## acceptance

The feature is done when all of the following hold, each measured against something that exists.

1. **<clause>** - <what is measured, and against what>.
2. **THE USER'S ACCEPTANCE** of the delivered behaviour.

## open questions

Each with what it blocks and who or what settles it. A question whose answer changes the shape of the work is asked before that work starts.

## deliberately NOT in scope

What was considered and excluded, so it is not re-proposed.
