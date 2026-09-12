---
name: xcalibre-dev
description: Declarative context vault for substantive engineering work that must survive sessions. Use for features, phases, refactors, and debugging campaigns larger than a one-off fix; not for questions, reviews, or trivial edits.
---

# Context Vault protocol

This skill defines persistent records, not an execution method. User prompts determine how work is performed. Project, language, and machine facts belong in `dev/gotchas.md`; binding requirements and vocabulary belong in `dev/spec.md`. Nothing in this skill is specific to a language, domain or repository; a helper, budget or convention that only makes sense in one project belongs in that project's `dev/`, never here.

## How to read these rules

NOT EVERY RULE HERE IS THE SAME KIND OF RULE, and treating them alike is what makes a session slow.

**Narrow bridge - follow exactly.** The header and its `LOAD` line, one fact one home, ID allocation and terminal states, plan filenames, the entry forms `check` enforces, the budgets, and landing work. Variation here costs another session a record it cannot read, so there is one right way and no judgment is asked for.

**Open field - direction, not law.** How a mechanism is chosen, how a candidate is weighed, which of two defensible designs to build, how much a question is worth measuring, and how much ceremony a piece of work deserves. Many paths reach the outcome; take the shortest one that leaves the records above true. AN ABSENT RULE IS FREEDOM, NOT AN OMISSION TO BE FILLED WITH CAUTION: do not invent a bar this file does not state, and do not ask it for permission it does not withhold.

`Pace` below is the boundary. It says what a step must DECLARE - its mechanism, its bar, its cost - never what a step must DO.

THE RECORDS ARE FOR PEOPLE AND FOR THE NEXT SESSION; THEY ARE NOT A GAG ORDER. Every record but the spec's binding core describes the route as it was understood when it was written, and a session holding better evidence amends it in the same commit as the change, with a decision saying why. Nothing in this file withholds from an agent the freedom to explore, measure and replace a mechanism, a plan or a clause; it asks only that the replacement be recorded so the next reader is not misled.

## Vault contract

`dev/activeContext.md` is the single live entry point. Its header is:

```yaml
LOAD: dev/activeContext.md, dev/spec.md, dev/architecture.md, dev/roadmap.md, dev/phaseRoadmap.md, dev/gotchas.md
updated: <ISO-8601 timestamp>
STATE: <PLANNING|REVIEWING|BUILDING|GATING|COMMITTING|BLOCKED|IDLE>
STEP: <stable step id and title>
HEAD: <git SHA at this write>
BRANCH: <working branch>
GATE: <verification command or none>
resume: <exact next action>
```

State meanings are data: `PLANNING` design is open; `REVIEWING` a review is pending; `BUILDING` has an in-flight diff; `GATING` verification is running or awaiting interpretation; `COMMITTING` is landing a completed change, which is COMMITTED AND PUSHED and not one without the other; `BLOCKED` records the blocker and what was attempted, and is for work that CANNOT proceed - never for a session that chose to pause, and never while an adviser or a cheaper experiment is still untried; `IDLE` has no in-flight step. A `HEAD` mismatch is reconciled against Git, which is authoritative for landed work. When the current milestone has a live plan, append that plan's path to `LOAD`. A record that is not in `LOAD` is a record that will be missed: anything meant to bind every session must be listed there.

`activeContext.md` holds what changes the NEXT action and nothing else. It is not a digest of `decisions.md`, a summary of the plan or a history of the phase - a line belongs there only if a cold session would take a different next step without it, and it CITES the record that owns the rest. Duplicated there, a fact goes stale in one copy while the other is amended. AND IT IS NOT APPEND-ONLY: a block a later record supersedes is DELETED in the same edit that adds its successor, and a budget that forces a session to shuffle blocks to admit one more is a record still carrying HISTORY - which belongs in `decisions.md` and `telemetry/`, both of which the deleted block already cites.

One fact has one home:

| Record | Owns |
|---|---|
| `dev/SCHEMA.md` | Vault manifest and project-specific budget exceptions |
| `dev/activeContext.md` | Current state, blocker, attempts, exact resumption |
| `dev/roadmap.md` | Project-wide phases, long-range milestones, and progress |
| `dev/phaseRoadmap.md` | The single active phase: deliverables, ordered work, and exit gate |
| `dev/plans/<milestone>.md` | Optional live plan: approach, substeps, open questions, and plan-local checks |
| `dev/spec.md` | What the delivered product must be true of: requirements, vocabulary, acceptance criteria. Its BINDING CORE outranks every other record; the rest is amended on evidence |
| `dev/architecture.md` | Current system structure, mechanisms, and data flow |
| `dev/gotchas.md` | Durable traps, environment constraints, and how to work in this project |
| `dev/decisions.md` | Append-only decision log: one short entry per decision, including refuted approaches |
| `dev/telemetry/` | Append-only measurements and gate results |
| `dev/scripts/` | Indexed, project-specific reusable development helpers |
| `dev/features/<slug>/` | One feature's own vault: the same records, scoped to that feature |
| `dev/archive/` | Historical, non-authoritative records |

The phase roadmap owns milestone order and status; a linked milestone plan owns how that milestone will be carried out; active context owns the exact next action. Plans are `### Plans` below.

## Phases, milestones and steps

Three units, three scopes, and each owns a different record:

| Unit | Is | ID | Lives in | Closes when |
|---|---|---|---|---|
| **Phase** | a stage of the whole project; one is active at a time | `P<n>` | a row in `roadmap.md`, expanded in `phaseRoadmap.md` while it is the active one | its exit gate passes |
| **Milestone** | a deliverable inside a phase that can be accepted or refused on its own | `P<n>-M<k>` | a row in `phaseRoadmap.md`, plus a plan where it needs one | its own stated exit criterion is met |
| **Step** | one commit-sized change with one verdict | `P<n>-M<k>-S<j>` | its milestone's plan, or rows under the roadmap row when there is no plan | it lands or is refused, with a decision id |

A unit also closes by taking a terminal state - superseded, absorbed, withdrawn or deferred - which is as legitimate an ending as delivering it, and is how a route the evidence has overtaken gets out of the way.

A FEATURE gets a VAULT OF ITS OWN, and opening one is the first act of building it - see below.

### The plan is a hypothesis, not a contract

THE ROADMAP RECORDS THE BEST ROUTE KNOWN WHEN IT WAS WRITTEN, AND EVIDENCE OUTRANKS IT. Any phase, milestone or step may be re-scoped, split, absorbed, deferred or withdrawn the moment the work shows it should be; that is what the terminal states above are for, and reaching for one is an ordinary act rather than an admission. A step the evidence has made pointless is CLOSED AS WITHDRAWN with the finding that killed it, never completed for the sake of the tick, and a finding that reshapes the phase reshapes the phase.

A MILESTONE DECLARES ITS SIZE WHEN IT OPENS AND IS SPLIT RATHER THAN GROWN. Its plan states, in the row that opens it, how many steps its deliverable is expected to take. Exceeding that is not forbidden and is not a failure - it is a TRIGGER that fires once: the session stops writing the next row and instead takes one of three decisions, recorded with the count that fired it - SPLIT the remainder into a new milestone with its own ID, CLOSE this one as delivered at what it has and forward the rest to a named row, or RESTATE the mechanism because a milestone that keeps needing another row has the wrong vocabulary. A MILESTONE WHOSE STEP LIST GROWS WHILE ITS EXIT CRITERION STANDS STILL HAS BECOME A PHASE, and the tell is countable: steps landed since the exit criterion last moved. Splitting costs one ID and one line; not splitting costs a milestone nobody can finish or refuse.

DO NOT STOP AT A BOUNDARY YOU CAN CROSS. Landing a step is not a reason to end a session and neither is closing a milestone: record it, push it, and carry on to whatever the goal needs next while you can still do it well. These units exist to make work legible to the session that follows, not to portion out how much of it any one session may do.

ASK FOR HELP BEFORE ASKING THE USER, AND BEFORE THE THIRD FORM. Consulting an adviser, delegating a search, or running work through other agents is available wherever the environment offers it, and it is NOT a last resort reserved for a blocker - a second opinion on a design costs less than one refuted build. FOUR TRIGGERS, and a session that meets one and does not reach for help has chosen the slower route: (i) a mechanism's SECOND form has been refused, before a third is written; (ii) two defensible mechanisms are open and the measurement that separates them costs more than an opinion; (iii) an implementation of the same problem is available to read, which is the rule below; (iv) the session is about to record that something has NO instrument, NO mechanism or NO precedent. IT IS NOT A PER-STEP CEREMONY: a step whose mechanism is obvious and whose cost is small asks nobody, and asking at every step is its own kind of slow.

THERE ARE THREE REASONS TO STOP, and the record says which:
- **A decision is genuinely the user's** - it changes what gets built, nothing available in the session settles it, and an adviser has not settled it either. Do everything that does not depend on the answer first, then ask one clear question.
- **The working context has degraded** - findings are being re-derived, or the session is holding more than it can hold accurately. Leave `activeContext.md` pointing at the exact next action and hand off.
- **A remaining budget is close to spent**, where the environment exposes one to read. Land and push what is finished, write the resumption, and stop with room in hand rather than mid-step. Where no such reading is available, the second reason covers it.

Anything else - a step boundary, a milestone boundary, a plan that has run out of rows - is a reason to write the next row, not a reason to stop.

### IDs are allocated, never renumbered

`<n>`, `<k>` and `<j>` are integers taken in allocation order and NEVER reused, renumbered or reordered. POSITION IN THE LIST IS ORDER; THE ID IS IDENTITY. Separating those two is what makes a rescope traceable: a milestone that belongs between `P2-M3` and `P2-M4` is written there in the list and takes the next free number - no decimals, no letter suffixes, no `M3a`.

A milestone or step is never deleted and never silently rewritten. It keeps its line and takes a terminal state:

```text
- [x] P2-M4 <title> - <what it delivered>
- [ ] P2-M5 <title>
- [-] P2-M6 <title> - SUPERSEDED BY P2-M9 (D204)
- [-] P2-M7 <title> - ABSORBED BY P2-M9 (D204)
- [-] P2-M8 <title> - WITHDRAWN (D318)
- [-] P2-M9 <title> - DEFERRED TO P3 (D207)
```

`[ ]` open, `[x]` closed as delivered, `[-]` closed without delivering. Every `[-]` names WHERE the work went and the decision that moved it, so a reader following a citation to a milestone that no longer does what its name says finds a forwarding line rather than nothing. Amending scope WITHIN a milestone's stated outcome is an edit plus a decision id; changing the outcome is a NEW ID and a terminal state on the old one. The same rule governs steps inside a plan.

An ID that predates this convention is GRANDFATHERED, never renamed - other records cite it - and the phase roadmap lists it beside its successor so the lineage is readable.

`phaseRoadmap.md` declares which phase it expands on a `phase: P<n> - <title>` line, and that phase has a row in `roadmap.md`. Between phases it declares `phase: none`.

### Plans

One plan per milestone, and only where the detail would crowd the phase roadmap:

```text
dev/plans/<milestone id, lowercased>-<short-slug>.md     e.g. dev/plans/p2-m1-cache-eviction.md
```

The filename carries the ID, so a plan is traceable to its row by name alone and the human-readable slug is never the only identifier. A plan names its milestone ID and title on its first line, is linked from that roadmap row, and is appended to `activeContext.md`'s `LOAD` while it is live. At milestone close it moves UNDER THE SAME NAME to `dev/archive/plans/<phase>/` and the roadmap row keeps the link. Reviews of a plan go to `dev/archive/reviews/<phase>/`, never beside the live plan.

### Opening a feature

`init --feature <slug>` creates a vault for that feature at `dev/features/<slug>/`, beside the project's own, and IS `dev/` when the project has no vault yet - so a feature is how a project acquires one. Every record, budget, ID rule and check in this file applies inside it unchanged; `check`, `resume` and `plan` take `--feature <slug>`.

THE VAULT IS THE FEATURE'S, AND SO IS ITS SPEC: it states what THE FEATURE must be true of, naming the project's requirements and the existing code's behaviour as INHERITED CONSTRAINTS it may not break. Its records are filled in a fixed ORDER - the request verbatim, then the host survey read off the CODE, then where the feature attaches and what that choice costs, then the feature's own spec, then its milestones - because that order is what stops an invention being recorded as a requirement.

**Opening, writing or closing one: read [reference/opening-a-feature.md](reference/opening-a-feature.md).**

### Starting, adopting, extending

- `init` scaffolds a project vault into a repository that has none: every record below, from the templates in `<skill-dir>/reference/`, with phase `P1` open and nothing invented.
- `init --feature <slug>` does the same for one feature, as above.
- `migrate` adopts an existing `dev/` - it renames legacy core files, converts flat JSON baselines and archives legacy fragments. Run it dry first and read what it would do.
- Work that is not a feature and not a phase - a refactor, a debugging campaign - is a MILESTONE of the active phase in the vault that owns the code.

## What a requirement is (`dev/spec.md`)

`dev/spec.md` states WHAT THE DELIVERED PRODUCT MUST BE TRUE OF. It is a record for a HUMAN READER of what the product promises, and the one record a session may use to REFUSE a change: a change that breaks a binding clause is refused, and nothing else is refused on the strength of this file. It is not an instruction set for agents, and it never says how the product is built.

One test admits a clause: **could a completely different implementation satisfy it?** If not, it is not a requirement.

Belongs in spec: externally observable behaviour and outputs; acceptance criteria and the numeric bars that decide them; supported inputs and the failures they must return; the public interface's promises; vocabulary; explicit non-goals.

Does NOT belong in spec, and each has a home: named functions, types, variables, flags, files and call order, and the internal mechanism generally (`architecture.md`); how to build, run, gate, measure or search for an answer (`gotchas.md`); why a mechanism was chosen or refused (`decisions.md`); what is being worked on and in what order (`phaseRoadmap.md` and plans); measurements themselves (`telemetry/`). AND NEITHER DOES PROCESS: who owns a clause, which milestone serves it, the date a ruling was made, what is "unbuilt until", what is "frozen", and how an earlier version of the clause read. Those are `phaseRoadmap.md` and `decisions.md`, and a spec that carries them has become a diary.

A SPEC HAS A BINDING CORE AND AN AMENDABLE REST, AND SAYS WHICH IS WHICH. The binding core is the handful of clauses that define the product - for a mesher, conformality, validity and capture; for a compiler, correctness - and no session relaxes it. Every other clause is amendable by the session holding the evidence: amend it under its own ID with a decision saying why, in the same commit as the change. A CANDIDATE IS NEVER REFUSED FOR DEPARTING FROM AN AMENDABLE CLAUSE OR FROM THE CURRENT ARCHITECTURE; it is measured, and the record follows the measurement. A spec whose clauses cannot all be read in five minutes has stopped being one: tens of clauses, not hundreds.

A requirement that prescribes a mechanism forecloses cheaper and better ones, and a spec that grows into an implementation manual is the most common way this vault slows a project down: candidate ideas get refused for departing from a clause that was never about the product. A CLAUSE FOUND NAMING A MECHANISM IS MOVED ON SIGHT, by whoever finds it, to `architecture.md` with a decision - no permission is needed, because the clause was never a requirement. When a mechanism is genuinely load-bearing, spec states the OUTCOME and `architecture.md` states the mechanism; spec may cite it but never restates it. An acceptance list is amended the same way, by a decision that names what changed; it is never frozen.

Requirement IDs are stable and permanent. Amend the text under its existing ID, record repeals in place, and never renumber - every other record cites them.

ONE FORM, ENFORCED, so the file can be scanned rather than read:

```text
<ID> <WHAT IT ENFORCES, IN CAPITALS> - <what must be true, briefly>.
```

ONE LINE, and at most 480 characters - what "four lines" meant. The capitalised clause is what the requirement enforces; the statement is an outcome, and it NEVER NAMES A KEYWORD, FUNCTION, FILE, CONSTANT OR STAGE ORDER - an API's keywords are documentation, and documentation is not a requirement. A clause lifted out because it states a second thing takes its parent's ID plus a letter - `R37b` - so lineage is in the name and every citation of the original still lands beside it. Anything longer is architecture, method or a decision. `check` enforces the head, the capitals, the cap, unique IDs, and the sections every spec carries: goal, vocabulary, priority, quality bars, requirements and acceptance.

## What a decision is (`dev/decisions.md`)

Append-only. One entry per decision, on **one line of at most 800 characters**:

```text
- <YYYY-MM-DD> D<N> <what was decided> - why: <the fact that decided it>
```

`D<N>` increases by one and is never reused. The `why` is the deciding evidence in as few words as carry it - a number, a count, a failure - not the reasoning that reached it. Evidence lives where evidence lives: cite a telemetry path, a commit SHA, a script or a requirement ID instead of inlining measurements, tables or narrative. A refused approach is recorded the same way and keeps the one number that killed it, so that it is not re-attempted.

This record is read by SEARCH, not by reading: `grep -n 'D203' dev/decisions.md` returns the whole entry, which is why it is never wrapped. Anything needing more than that is not a decision entry - it is a plan, an architecture note, a telemetry artefact or a gotcha, and it goes there with the entry citing it. `check` enforces the entry shape, the one-line form, the character cap, the `why`, and monotonic IDs.

At phase close, the phase's entries move to `dev/archive/phases/<phase>/decisions.md` and the live file restarts at D1.

## Budgets

Default limits are 60 lines for `activeContext.md`, 90 for `gotchas.md`, 100 for `architecture.md`, 120 each for `roadmap.md` and `phaseRoadmap.md`, 120 for `spec.md`, 150 for live milestone plans, and 50 for `SCHEMA.md`. `decisions.md` and `telemetry/` have no total limit; `decisions.md` is bounded per entry instead. A repository may declare a justified exception in `SCHEMA.md`, which is a one-line entry and not a decision. Excess narrative belongs in `decisions.md` or `archive/`, according to whether it remains authoritative.

**A BUDGET IS A SIGNAL TO SPLIT OR ARCHIVE AND NEVER TO DELETE BINDING CONTENT.** `gotchas.md` in particular grows monotonically with a project's age - every line is a trap that already cost a session - so a budget that forces one out is the budget costing more than it saves. When a record is full, raise its ceiling in `SCHEMA.md`, move the historical half to `archive/`, or split the record; a session that spends three edits merging and re-splitting binding lines to admit one more has been slowed by the rule that was meant to speed it up. AND A TRAP THAT IS NO LONGER TRUE COSTS MORE THAN NO TRAP: `gotchas.md` is RE-READ and corrected, not appended to blindly, and a line a later measurement disproved is fixed in place - a stale trap buys permanent defensive checking against a defect that no longer exists.

**A COMMENT IS A COMMENT, NOT A NARRATIVE - THREE LINES, HARD.** No comment in source may exceed three lines, anywhere, in any language, and **A BLANK LINE DOES NOT END A COMMENT AND DOES NOT RESET THE COUNT: what is counted is every consecutive comment line up to the next line of CODE, however it is spaced.** Splitting a nine-line narrative into three paragraphs is the same nine lines and is refused; only code ends a comment. **AND A COMMENT CARRIES NO NARRATIVE AND NO CASE SPECIFICS - ONLY WHAT THE IMPLEMENTATION IS.** An invariant, a unit, a bound, a trap, a refused alternative in one clause. A NUMBER MEASURED ON A CASE IS NOT AN IMPLEMENTATION FACT: no case name, no before-and-after figure, no history of what was tried, no account of what a run showed. Those belong to `decisions.md` and `telemetry/`, and a comment that needs them CITES a `D<n>` instead of restating them. The test is whether the line would still be true of a different input; if it names an input, it is evidence and has another home. A comment that has grown past three lines is a decision entry that was written in the wrong file: move it, and leave the one line that tells the next reader what they must not break. `check` ENFORCES all of this over the whole repository, in every language it knows a comment prefix for, and `scripts/comment_blocks.py <file> --over 3` dumps the offenders with their line ranges so they can be rewritten by range.

**AND A DOCSTRING IS FOR THE PUBLIC API, NOTHING ELSE.** A function, type or constant the user cannot call is documented in COMMENTS and never in a docstring, whatever the language's convention - a docstring on an internal is the three-line rule evaded by changing the delimiter, and it publishes an internal as though it were part of the interface. The same three-line limit binds every comment that replaces one. What legitimately keeps a docstring is what the user's own interface exposes, and it documents the CONTRACT - arguments, returns, failures - never the mechanism.

**ONE BLOCK, ONE LINE, AND A BLOCK IS BOUNDED.** A paragraph, list item, table row, requirement or decision entry is ONE source line and is never hard-wrapped by hand: a sentence broken across lines cannot be read or edited as prose, and every edit then costs a reflow. Let the editor wrap it. What IS bounded is the block - 2,600 characters - because a line count over hand-wrapped text measures the wrapping and not the content, which is how one record came to hold a 7,414-character table cell inside a 100-line budget. A requirement is bounded at 480 and a decision entry at 800, which is what "four lines" and "three lines" meant. `check` enforces all four.

**AND THE BOUND IS PER RECORD**, because a 120-line record of 2,600-character blocks is a 300-kilobyte record that every session pays to read: 900 characters for a block of `activeContext.md`, 1,200 for a row of `roadmap.md` or `phaseRoadmap.md`, 1,600 for a block of `architecture.md` or of a live plan, and 2,600 elsewhere; table rows are exempt. A row over its cap is a plan, a decision or a telemetry artefact written in the wrong record, and the row CITES it instead. `check` enforces the caps.

## Pace

The records above are what a session leaves behind; these rules keep the work from slowing into case-by-case legislation, and a plan that breaks one is refused at review, not at the gate.

- A RECORD IS NOT A REFUSAL. A plan is refused at review for breaking a BINDING clause of the spec, for stating no bar, or under the patch rule below - never for departing from `architecture.md`, from an amendable clause or from the roadmap's route. Those records are amended by the step that measures better, in the same commit, and a refusal whose only ground is one of them is itself the defect.
- A RULE IS A MECHANISM'S CONSEQUENCE OR IT IS A PATCH. A step's row names the mechanism its change follows from - an invariant that holds on every configuration carrying it - and a change that adds a priority between named situations, or a branch keyed on one property that cannot tell the configuration it was built on from another carrying the same property, is refused at DESIGN time and recorded as refused, with the configuration it would have confused.
- A TIE-BREAK THAT CHANGES THE ANSWER IS THE RULE DOING NOTHING. Where a pass picks among candidates - the lowest index, the first found, the nearest - RUN IT ONCE WITH THE PICK REVERSED. If the verdict moves, the pick and not the invariant was deciding, and the rule is a patch however principled its predicate reads. The fix is never a better tie-break: state what the pass must LEAVE TRUE of the object it builds, test exactly that, and let a fixpoint settle which candidate goes - the pick then stops mattering, and the cascade is bounded by the rounds the loop already has. THIS COSTS ONE RUN and it is the cheapest refutation in this file.
- A PROBLEM SOMEONE ELSE HAS SOLVED IS READ, NOT RE-DERIVED. Where an implementation of the same problem is on the machine or in the repository's own history - a comparator's source, a prior branch, a deleted operator - READ IT BEFORE DESIGNING A MECHANISM, and read its SOURCE and not only its output. Its output answers what it PRODUCED and costs a full run per question, often ambiguously; its source answers what it DOES in minutes and states outright the bound, the order of operations, the arity split and the fallback that no output can show. A step that refutes its own form on a question an available source already answers has bought a measurement it did not need, and that is the most expensive avoidable error this file knows. What the source says is recorded ONCE as a decision naming the file and line, so the next session reads the decision and not the source.
- THE CONFIGURATION SPACE IS ENUMERATED, NOT DISCOVERED. Work on a class of defects states that class's configuration space in the plan as a product of named parameters - written as it becomes known, not demanded before anything may begin - and the milestone owns a GENERATED catalogue of fixtures over that product, run as ONE table; the gate is the table, never one hand-built case at a time. A defect found on a case adds a ROW, not a case, and a parameter the catalogue lacks is the finding. A candidate is SCREENED on the rows its own mechanism can reach, which is a reading and never a verdict.
- VERIFICATION IS PROPORTIONATE TO WHAT THE CHANGE CAN REACH, AND THE FULL TABLE GATES THE MILESTONE AND NOT EVERY STEP. A step's row states its BLAST RADIUS and the diff proves it, and that radius - never habit - sets what the step pays at its close. A step that writes no shipped output verifies THAT it wrote none, plus the rows its own mechanism reaches. A step that changes one mechanism verifies that mechanism's population and the regression floor. Only a step changing shipped output on a population it cannot bound owes the whole table. THE FULL TABLE, THE FULL REGRESSION FLOOR AND THE EXPENSIVE END-TO-END CASES RUN ONCE AT THE MILESTONE'S CLOSE and at a phase's gate - not once per step, and never once per form. A verification run no result of which could change a verdict is not rigour and buys nothing; run per step it multiplies a milestone's cost by its step count, and it is reliably the largest removable cost in an iterating session.
- EVERY DETERMINISTIC ASSIGNMENT HAS A CONTINUOUS FALLBACK. Where a target is unreachable under a validity guard, the next step is the mechanism that relaxes the surrounding state, never another priority. The same assignment rewritten three times is the signal that the vocabulary is wrong: the plan replaces the priorities with a stated objective or a solver and a decision says so.
- THE BAR AND THE COST ARE STATED BEFORE THE BUILD, AND THE BAR IS RANKED. Each step's row states what accepts or refuses it and the cost per unit of work it may add, before a line is written. A BAR IS NEVER FLAT: name the ONE class that is strict - the invariant nothing may break - and put every quantity below it in a band or an aggregate, because a bar written as "no number worse" or "every row improves" over a many-objective measurement is not rigour. It selects for candidates too timid to reach the defect, and refuses one that lifts most of the table for a fraction of a percent on a row nobody ranked. A candidate is measured ONCE against that bar FOR A VERDICT, screening aside; a session that iterates forms records ONE telemetry artefact for the sweep and one decision per refuted form, and stops at the THIRD FORM THAT DID NOT IMPROVE ON THE ONE BEFORE IT to restate the mechanism - three forms converging is convergence and continues, three forms trading one failure for another is thrashing and the vocabulary is wrong.
- A BAR, CONCRETELY. Refused: *"no number worse across the catalogue."* Written instead: *"strict - nothing the contract guarantees may break; the objective improves on the cases the mechanism actually reaches; every other measured quantity moves inside a stated band, with an attribution."* Same rigour, one class strict, the rest ranked.
- DIAGNOSTICS LIVE IN SCRIPTS. Trace flags, probes and one-off prints are removed from shipped code before a step lands; a probe worth repeating is indexed in `dev/scripts/`.
- CEREMONY IS BUDGETED. A decision is recorded where a rule changes or a mechanism is refused, never per probe; finalised cases and expensive baselines are re-measured ONCE at the MILESTONE's close, not at every step's end and never between forms; the exact resumption in `activeContext.md` is one action, not a narrative.

## Reporting to the user

The vault is what the next SESSION reads; a report is what the PERSON reads to decide what happens next, and the two are not the same document. Lead with what changed, then what it means, then what is next - in that order, briefly, in the project's own vocabulary.

- **WHAT WAS DONE** - the change itself, in a sentence or two.
- **WHAT IT MEANS** - the movement against the phase's own exit criterion, as a number that moved. WHERE NOTHING THE USER IS WAITING FOR MOVED, SAY SO IN ONE LINE and say what would move it; a step can be correct, gated and worth landing while moving no acceptance clause, and reporting it as progress it is not is how a phase's real position gets lost.
- **WHAT IS NEXT** - the one next action, plus anything only the user can decide.

REFUTATIONS ARE RECORDED, NOT RECOUNTED. A refuted form, a withdrawn step, a bar that failed: these belong in `decisions.md` and the telemetry artefact, where they stop the next session repeating them. A report names one only where the user's next decision turns on it. A report that spends its length on what did not work reads as a phase in trouble even when the phase is on track, and it buries the line the user actually needed. THIS IS A CHANGE OF EMPHASIS AND NEVER OF RIGOUR: nothing is hidden or softened, a result is never overstated, and a failure the user must act on is the FIRST line rather than the last.

## Landing work

**WORK THAT IS NOT PUSHED IS NOT LANDED.** A step ends as a commit on the working branch AND a push to that branch's upstream, in one act: `COMMITTING` is not finished until the remote carries it. Commit and push AT EACH LANDED STEP, while the session runs, never in one batch at its end - a session that ends with work only in the working tree, or only in local commits, has left nothing another session or another machine can read, and a `HEAD` written into `activeContext.md` that no remote carries is a citation that cannot be followed. A branch with no upstream is given one when its first step lands, not later.

A PUSH THAT FAILS IS A FACT OF THE VAULT, NOT A DETAIL TO RETRY IN SILENCE. Rejected, unauthenticated, protected, no remote: the commit stands, `activeContext.md` takes `STATE: BLOCKED` with the failure and what was attempted, and the user is told in the session rather than at its end. `resume` prints the count of unpushed commits, so a cold session sees at once what the last one left behind.

Commit authorship and any attribution trailer follow the repository's own convention and the environment's instructions; this file does not set them.

## Interface

Run from any checkout; `<skill-dir>` is the directory containing this file.

```text
<skill-dir>/scripts/xcalibre-dev init [--feature <slug>] [repository]
<skill-dir>/scripts/xcalibre-dev plan <milestone-id> <slug> [--feature <slug>] [repository]
<skill-dir>/scripts/xcalibre-dev resume [--full] [--feature <slug>] [repository]
<skill-dir>/scripts/xcalibre-dev check [--feature <slug>] [repository]
<skill-dir>/scripts/xcalibre-dev migrate [repository]
<skill-dir>/scripts/xcalibre-dev migrate --apply [repository]
```

`init` scaffolds a vault from `<skill-dir>/reference/` and never overwrites an existing record; `--feature <slug>` makes it that feature's own vault. `plan` creates a milestone plan under the one legal name. `resume` emits Git facts, then the two records a session must have READ BEFORE IT ACTS - `activeContext.md`, which says what to do next, and `gotchas.md`, which says how work is done here: the evidence ladder, the cheapest artefact that answers a question, what a gate is and is not for. The other `LOAD` records are consulted on demand and are manifested by name and size; `--full` emits every one of them as a context packet. `check` validates the schema, header, paths, budgets and block form, telemetry headers, the `spec.md` and `decisions.md` entry formats, and the phase/milestone/plan naming above. IT IS A LOOP AND NOT A FINAL EXAM: run it, fix exactly what it names, run it again, and only then commit. It exits non-zero on INVALID, so `check && commit` is safe - but a PIPELINE's status is its LAST command's, so a status read through `| tail` is that tool's and says nothing about the vault. `migrate` is dry-run by default; `--apply` renames legacy core files, converts flat JSON baselines, and archives legacy `phase*.md` fragments while preserving linked milestone plans.

## Maintaining this skill

A helper belongs in the repository unless it is project-, domain- and language-neutral. The canonical copy is this skill inside the packaged repository. Marketplace installations must not be edited or synchronised directly. **Before and after any edit: read [reference/maintaining-the-skill.md](reference/maintaining-the-skill.md).**

Source comments do not carry transient vault step or decision IDs.
