---
name: xcalibre-dev
description: Declarative context vault for substantive engineering work that must survive sessions. Use for features, phases, refactors, and debugging campaigns larger than a one-off fix; not for questions, reviews, or trivial edits. Direct invocation only — do not select automatically.
---

# Context Vault protocol

This skill defines persistent records, not an execution method. User prompts determine how work is performed. Project, language, and machine facts belong in `dev/gotchas.md`; binding requirements and vocabulary belong in `dev/spec.md`. Nothing here is specific to a language, domain or repository; a helper, budget or convention that makes sense in only one project belongs in that project's `dev/`, never here.

## How to read these rules

NOT EVERY RULE HERE IS THE SAME KIND OF RULE; treating them alike slows a session.

**Narrow bridge - follow exactly.** The header and its `LOAD` line, one fact one home, ID allocation and terminal states, plan filenames, the entry forms `check` enforces, the budgets, and landing work. Variation costs another session a record it cannot read: one right way, no judgment asked.

**Open field - direction, not law.** How a mechanism is chosen, how a candidate is weighed, which of two defensible designs to build, how much a question is worth measuring, and how much ceremony a piece of work deserves. Many paths reach the outcome; take the shortest that leaves the records above true. AN ABSENT RULE IS FREEDOM, NOT AN OMISSION TO BE FILLED WITH CAUTION: do not invent a bar this file does not state, and do not ask it for permission it does not withhold.

`Pace` below is the boundary. It says what a step must DECLARE - its mechanism, its bar, its cost - never what a step must DO.

THE RECORDS ARE FOR PEOPLE AND FOR THE NEXT SESSION; THEY ARE NOT A GAG ORDER. Every record but the spec's binding core describes the route as understood when written; a session holding better evidence amends it in the same step as the change, with a decision saying why. Nothing here withholds the freedom to explore, measure and replace a mechanism, a plan or a clause; it asks only that the replacement be recorded so the next reader is not misled.

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

State meanings are data: `PLANNING` design is open; `REVIEWING` a review is pending; `BUILDING` has an in-flight diff; `GATING` verification is running or awaiting interpretation; `COMMITTING` is landing a completed change, which is COMMITTED AND PUSHED and not one without the other; `BLOCKED` records the blocker and what was attempted, and is for work that CANNOT proceed - never for a session that chose to pause, and never while an adviser or a cheaper experiment is still untried; `IDLE` has no in-flight step. A `HEAD` mismatch is reconciled against Git, which is authoritative for landed work. When the current milestone has a live plan, append its path to `LOAD`. A record not in `LOAD` will be missed: anything meant to bind every session must be listed there.

`activeContext.md` holds what changes the NEXT action and nothing else. It is not a digest of `decisions.md`, a plan summary or a phase history - a line belongs there only if a cold session would take a different next step without it, and it CITES the record that owns the rest; a duplicated fact goes stale in one copy. AND IT IS NOT APPEND-ONLY: a block a later record supersedes is DELETED in the same edit that adds its successor. A budget that forces shuffling blocks to admit one more means the record still carries HISTORY, which belongs in `decisions.md` and `telemetry/`.

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
| `dev/features/INDEX.md` | Which project branch each feature is built on, and whether it is open |
| `dev/archive/` | Historical, non-authoritative records |

**THE VAULT IS ITS OWN REPOSITORY.** `dev/` is a separate Git repository with a private GitHub remote, and `/dev/` is in the project's `.git/info/exclude` (never its `.gitignore`), so vault history is kept and no vault file enters a project commit or pull request. `check` is INVALID while the project tracks a vault file; `git rm -r --cached dev` untracks it. THE VAULT REPOSITORY HAS ONE BRANCH: project branches are told apart by feature vaults and their index rows, never by vault branches, so every feature's records travel in one history.

## First use

Run `doctor`. If it reports anything missing, ask the user once to agree to installing it and creating a private vault repository on their GitHub account, then install with the commands it prints, run `gh auth login` if needed, and run `init --remote`. On a new machine `init --remote` clones the existing vault. An existing `dev/` is adopted the same way: `init` keeps every record, and `resume` confirms `dev/` is ignored and names any tracked vault file to untrack.

The phase roadmap owns milestone order and status; a linked milestone plan owns how that milestone will be carried out; active context owns the exact next action. Plans are `### Plans` below.

## Phases, milestones and steps

Three units, three scopes, and each owns a different record:

| Unit | Is | ID | Lives in | Closes when |
|---|---|---|---|---|
| **Phase** | a stage of the whole project; one is active at a time | `P<n>` | a row in `roadmap.md`, expanded in `phaseRoadmap.md` while it is the active one | its exit gate passes |
| **Milestone** | a deliverable inside a phase that can be accepted or refused on its own | `P<n>-M<k>` | a row in `phaseRoadmap.md`, plus a plan where it needs one | its own stated exit criterion is met |
| **Step** | one commit-sized change with one verdict | `P<n>-M<k>-S<j>` | its milestone's plan, or rows under the roadmap row when there is no plan | it lands or is refused, with a decision id |

A unit also closes by taking a terminal state - superseded, absorbed, withdrawn or deferred - as legitimate an ending as delivering it; it is how a route the evidence has overtaken gets out of the way.

A FEATURE gets a VAULT OF ITS OWN, and opening one is the first act of building it - see below.

### The plan is a hypothesis, not a contract

THE ROADMAP RECORDS THE BEST ROUTE KNOWN WHEN IT WAS WRITTEN, AND EVIDENCE OUTRANKS IT. Any phase, milestone or step may be re-scoped, split, absorbed, deferred or withdrawn the moment the work shows it should be; reaching for a terminal state is an ordinary act, not an admission. A step the evidence made pointless is CLOSED AS WITHDRAWN with the finding that killed it, never completed for the tick, and a finding that reshapes the phase reshapes the phase.

A MILESTONE DECLARES ITS SIZE WHEN IT OPENS AND IS SPLIT RATHER THAN GROWN. Its plan states, in its opening row, how many steps the deliverable is expected to take. Exceeding that is not forbidden or a failure - it is a TRIGGER that fires once: the session stops writing the next row and takes one of three decisions, recorded with the count that fired it - SPLIT the remainder into a new milestone with its own ID, CLOSE this one as delivered at what it has and forward the rest to a named row, or RESTATE the mechanism, because a milestone that keeps needing another row has the wrong vocabulary. A MILESTONE WHOSE STEP LIST GROWS WHILE ITS EXIT CRITERION STANDS STILL HAS BECOME A PHASE; the tell is countable: steps landed since the exit criterion last moved. Splitting costs one ID and one line; not splitting costs a milestone nobody can finish or refuse.

DO NOT STOP AT A BOUNDARY YOU CAN CROSS. Neither landing a step nor closing a milestone is a reason to end a session: record it, push it, and carry on to whatever the goal needs next while you can still do it well. These units make work legible to the next session; they do not ration any one session's work.

ASK FOR HELP BEFORE ASKING THE USER, AND BEFORE THE THIRD FORM. Consulting an adviser, delegating a search, or running work through other agents, wherever the environment offers it, is NOT a last resort for a blocker - a second opinion costs less than one refuted build. FOUR TRIGGERS; a session that meets one and does not reach for help has chosen the slower route: (i) a mechanism's SECOND form has been refused, before a third is written; (ii) two defensible mechanisms are open and the measurement that separates them costs more than an opinion; (iii) an implementation of the same problem is available to read, which is the rule below; (iv) the session is about to record that something has NO instrument, NO mechanism or NO precedent. IT IS NOT A PER-STEP CEREMONY: a step whose mechanism is obvious and cheap asks nobody; asking at every step is its own kind of slow.

THERE ARE THREE REASONS TO STOP, and the record says which:
- **A decision is genuinely the user's** - it changes what gets built, and neither the session nor an adviser can settle it. Do everything that does not depend on the answer first, then ask one clear question.
- **The working context has degraded** - findings are being re-derived, or the session holds more than it can hold accurately. Leave `activeContext.md` pointing at the exact next action and hand off.
- **A remaining budget is close to spent**, where the environment exposes one. Land and push what is finished, write the resumption, and stop with room in hand, not mid-step. Where no such reading exists, the second reason covers it.

Anything else - a step or milestone boundary, a plan out of rows - is a reason to write the next row, not to stop.

### IDs are allocated, never renumbered

`<n>`, `<k>` and `<j>` are integers taken in allocation order and NEVER reused, renumbered or reordered. POSITION IN THE LIST IS ORDER; THE ID IS IDENTITY. That separation makes a rescope traceable: a milestone belonging between `P2-M3` and `P2-M4` is written there in the list and takes the next free number - no decimals, no letter suffixes, no `M3a`.

A milestone or step is never deleted and never silently rewritten. It keeps its line and takes a terminal state:

```text
- [x] P2-M4 <title> - <what it delivered>
- [ ] P2-M5 <title>
- [-] P2-M6 <title> - SUPERSEDED BY P2-M9 (D204)
- [-] P2-M7 <title> - ABSORBED BY P2-M9 (D204)
- [-] P2-M8 <title> - WITHDRAWN (D318)
- [-] P2-M9 <title> - DEFERRED TO P3 (D207)
```

`[ ]` open, `[x]` closed as delivered, `[-]` closed without delivering. Every `[-]` names WHERE the work went and the decision that moved it, so a citation to a milestone no longer doing what its name says finds a forwarding line. Amending scope WITHIN a milestone's stated outcome is an edit plus a decision id; changing the outcome is a NEW ID and a terminal state on the old one. Steps inside a plan follow the same rule.

An ID that predates this convention is GRANDFATHERED, never renamed - other records cite it - and the phase roadmap lists it beside its successor so the lineage is readable.

`phaseRoadmap.md` declares which phase it expands on a `phase: P<n> - <title>` line, and that phase has a row in `roadmap.md`. Between phases it declares `phase: none`.

### Plans

One plan per milestone, and only where the detail would crowd the phase roadmap:

```text
dev/plans/<milestone id, lowercased>-<short-slug>.md     e.g. dev/plans/p2-m1-cache-eviction.md
```

The filename carries the ID, so a plan is traceable to its row by name alone, never by slug only. A plan names its milestone ID and title on its first line, is linked from that roadmap row, and is appended to `activeContext.md`'s `LOAD` while live. At milestone close it moves UNDER THE SAME NAME to `dev/archive/plans/<phase>/`; the roadmap row keeps the link. Reviews of a plan go to `dev/archive/reviews/<phase>/`, never beside the live plan.

### Opening a feature

`init --feature <slug> [--branch <name>]` creates a vault for that feature at `dev/features/<slug>/`, beside the project's own (scaffolded first when absent), and binds it to the project branch it is built on - the checked-out one by default - with a row in `dev/features/INDEX.md`. ONE OPEN FEATURE PER BRANCH, so several features are built at once, each on its own branch, and switching branch switches vault: `resume` and `plan` act on the feature bound to the checked-out branch, `--feature <slug>` overrides, and a branch with no open row uses the project vault. Every record, budget, ID rule and check in this file applies inside it unchanged; `check` reads every vault and the index.

THE VAULT IS THE FEATURE'S, AND SO IS ITS SPEC: it states what THE FEATURE must be true of, naming the project's requirements and the existing code's behaviour as INHERITED CONSTRAINTS it may not break. Its records are filled in a fixed ORDER - the request verbatim, then the host survey read off the CODE, then where the feature attaches and what that choice costs, then the feature's own spec, then its milestones - because that order stops an invention being recorded as a requirement.

**Opening, writing or closing one: read [reference/opening-a-feature.md](reference/opening-a-feature.md).**

### Starting, adopting, extending

- `init` scaffolds a project vault into a repository that has none: every record below, from the templates in `<skill-dir>/reference/`, with phase `P1` open and nothing invented.
- `init --feature <slug> [--branch <name>]` does the same for one feature, as above; on an existing feature it only adds a missing index row.
- `migrate` adopts an existing `dev/`: it renames legacy core files, converts flat JSON baselines and archives legacy fragments. Run it dry first and read what it would do.
- Work that is not a feature and not a phase - a refactor, a debugging campaign - is a MILESTONE of the active phase in the vault that owns the code.

## What a requirement is (`dev/spec.md`)

`dev/spec.md` states WHAT THE DELIVERED PRODUCT MUST BE TRUE OF, for a HUMAN READER: what the product promises. It is the one record a session may use to REFUSE a change: a change breaking a binding clause is refused, and nothing else is refused on the strength of this file. It is not an instruction set for agents and never says how the product is built.

One test admits a clause: **could a completely different implementation satisfy it?** If not, it is not a requirement.

Belongs in spec: externally observable behaviour and outputs; acceptance criteria and the numeric bars that decide them; supported inputs and the failures they must return; the public interface's promises; vocabulary; explicit non-goals.

Does NOT belong in spec, each with its home: named functions, types, variables, flags, files and call order, and the internal mechanism generally (`architecture.md`); how to build, run, gate, measure or search for an answer (`gotchas.md`); why a mechanism was chosen or refused (`decisions.md`); what is being worked on and in what order (`phaseRoadmap.md` and plans); measurements themselves (`telemetry/`). AND NEITHER DOES PROCESS: who owns a clause, which milestone serves it, the date a ruling was made, what is "unbuilt until" or "frozen", and how an earlier version of the clause read - those are `phaseRoadmap.md` and `decisions.md`; a spec carrying them has become a diary.

A SPEC HAS A BINDING CORE AND AN AMENDABLE REST, AND SAYS WHICH IS WHICH. The binding core is the few clauses defining the product - for a mesher, conformality, validity and capture; for a compiler, correctness - and no session relaxes it. Every other clause is amendable by the session holding the evidence, under its own ID, with a decision saying why, in the same step as the change. A CANDIDATE IS NEVER REFUSED FOR DEPARTING FROM AN AMENDABLE CLAUSE OR FROM THE CURRENT ARCHITECTURE; it is measured, and the record follows the measurement. A spec that cannot be read in five minutes has stopped being one: tens of clauses, not hundreds.

A requirement that prescribes a mechanism forecloses cheaper and better ones; a spec grown into an implementation manual - the commonest way this vault slows a project - refuses candidates over clauses never about the product. A CLAUSE FOUND NAMING A MECHANISM IS MOVED ON SIGHT, by whoever finds it, to `architecture.md` with a decision - no permission needed, since it was never a requirement. When a mechanism is genuinely load-bearing, spec states the OUTCOME and `architecture.md` the mechanism; spec may cite it but never restates it. An acceptance list is amended the same way, by a decision naming what changed; it is never frozen.

Requirement IDs are stable and permanent. Amend the text under its existing ID, record repeals in place, and never renumber - every other record cites them.

ONE FORM, ENFORCED, so the file can be scanned rather than read:

```text
<ID> <WHAT IT ENFORCES, IN CAPITALS> - <what must be true, briefly>.
```

ONE LINE, at most 480 characters (what "four lines" meant). The capitalised clause is what the requirement enforces; the statement is an outcome and NEVER NAMES A KEYWORD, FUNCTION, FILE, CONSTANT OR STAGE ORDER - an API's keywords are documentation, not requirements. A clause lifted out because it states a second thing takes its parent's ID plus a letter - `R37b` - so lineage is in the name and every citation of the original still lands beside it. Anything longer is architecture, method or a decision. `check` enforces the head, the capitals, the cap, unique IDs, and the sections every spec carries: goal, vocabulary, priority, quality bars, requirements and acceptance.

## What a decision is (`dev/decisions.md`)

Append-only. One entry per decision, on **one line of at most 800 characters**:

```text
- <YYYY-MM-DD> D<N> <what was decided> - why: <the fact that decided it>
```

`D<N>` increases by one and is never reused. The `why` is the deciding evidence, tersely - a number, a count, a failure - not the reasoning that reached it. Cite a telemetry path, commit SHA, script or requirement ID instead of inlining measurements, tables or narrative. A refused approach is recorded the same way, keeping the one number that killed it so it is not re-attempted.

This record is read by SEARCH, not by reading: `grep -n 'D203' dev/decisions.md` returns the whole entry, which is why it is never wrapped. Anything needing more is not a decision entry - it is a plan, architecture note, telemetry artefact or gotcha, and goes there with the entry citing it. `check` enforces the entry shape, the one-line form, the character cap, the `why`, and monotonic IDs.

At phase close, the phase's entries move to `dev/archive/phases/<phase>/decisions.md` and the live file restarts at D1.

## Budgets

Default limits are 60 lines for `activeContext.md`, 90 for `gotchas.md`, 100 for `architecture.md`, 120 each for `roadmap.md` and `phaseRoadmap.md`, 120 for `spec.md`, 150 for live milestone plans, and 50 for `SCHEMA.md`. `decisions.md` and `telemetry/` have no total limit; `decisions.md` is bounded per entry instead. A repository may declare a justified exception in `SCHEMA.md` as a one-line entry, not a decision. Excess narrative belongs in `decisions.md` or `archive/`, according to whether it remains authoritative.

**A BUDGET IS A SIGNAL TO SPLIT OR ARCHIVE AND NEVER TO DELETE BINDING CONTENT.** `gotchas.md` grows monotonically with a project's age - every line is a trap that already cost a session - so a budget forcing one out costs more than it saves. When a record is full, raise its ceiling in `SCHEMA.md`, move the historical half to `archive/`, or split the record; three edits spent merging and re-splitting binding lines to admit one more is the rule slowing the work it was meant to speed. AND A TRAP THAT IS NO LONGER TRUE COSTS MORE THAN NO TRAP: `gotchas.md` is RE-READ and corrected, not appended to blindly; a line a later measurement disproved is fixed in place, since a stale trap buys permanent defensive checking against a defect that no longer exists.

**A COMMENT IS A COMMENT, NOT A NARRATIVE - THREE LINES, HARD.** No comment in source may exceed three lines, anywhere, in any language, and **A BLANK LINE DOES NOT END A COMMENT AND DOES NOT RESET THE COUNT: what is counted is every consecutive comment line up to the next line of CODE, however it is spaced.** A nine-line narrative split into three paragraphs is still nine lines and is refused. **AND A COMMENT CARRIES NO NARRATIVE AND NO CASE SPECIFICS - ONLY WHAT THE IMPLEMENTATION IS.** An invariant, a unit, a bound, a trap, a refused alternative in one clause. A NUMBER MEASURED ON A CASE IS NOT AN IMPLEMENTATION FACT: no case name, no before-and-after figure, no history of what was tried, no account of what a run showed. Those belong to `decisions.md` and `telemetry/`; a comment that needs them CITES a `D<n>`. The test: would the line still be true of a different input? If it names an input, it is evidence and has another home. A comment past three lines is a decision entry in the wrong file: move it, and leave the one line that tells the next reader what they must not break. `check` ENFORCES all of this over the whole repository, in every language it knows a comment prefix for, and `scripts/comment_blocks.py <file> --over 3` dumps the offenders with their line ranges for rewriting by range.

**AND A DOCSTRING IS FOR THE PUBLIC API, NOTHING ELSE.** A function, type or constant the user cannot call is documented in COMMENTS, never a docstring, whatever the language's convention - a docstring on an internal evades the three-line rule by changing the delimiter, and publishes the internal as interface. The same three-line limit binds every comment that replaces one. What the user's own interface exposes keeps its docstring, which documents the CONTRACT - arguments, returns, failures - never the mechanism.

**ONE BLOCK, ONE LINE, AND A BLOCK IS BOUNDED.** A paragraph, list item, table row, requirement or decision entry is ONE source line, never hard-wrapped by hand - hand-wrapped prose cannot be read or edited as prose. Let the editor wrap it. What IS bounded is the block - 2,600 characters - because a line count over hand-wrapped text measures wrapping, not content; that is how one record came to hold a 7,414-character table cell inside a 100-line budget. A requirement is bounded at 480 and a decision entry at 800 (what "four lines" and "three lines" meant). `check` enforces all four.

**AND THE BOUND IS PER RECORD**, because a 120-line record of 2,600-character blocks is a 300-kilobyte record every session pays to read: 900 characters for a block of `activeContext.md`, 1,200 for a row of `roadmap.md` or `phaseRoadmap.md`, 1,600 for a block of `architecture.md` or of a live plan, and 2,600 elsewhere; table rows are exempt. A row over its cap is a plan, decision or telemetry artefact in the wrong record, and the row CITES it instead. `check` enforces the caps.

## Pace

The records above are what a session leaves behind; these rules keep the work from slowing into case-by-case legislation. A plan that breaks one is refused at review, not at the gate.

- A RECORD IS NOT A REFUSAL. A plan is refused at review for breaking a BINDING clause of the spec, for stating no bar, or under the patch rule below - never for departing from `architecture.md`, an amendable clause or the roadmap's route, which the step that measures better amends in the same step; a refusal grounded only in one of them is itself the defect.
- A RULE IS A MECHANISM'S CONSEQUENCE OR IT IS A PATCH. A step's row names the mechanism its change follows from - an invariant that holds on every configuration carrying it. A change that adds a priority between named situations, or a branch keyed on one property that cannot tell the configuration it was built on from another carrying the same property, is refused at DESIGN time and recorded as refused, with the configuration it would have confused.
- A TIE-BREAK THAT CHANGES THE ANSWER IS THE RULE DOING NOTHING. Where a pass picks among candidates - the lowest index, the first found, the nearest - RUN IT ONCE WITH THE PICK REVERSED. If the verdict moves, the pick and not the invariant was deciding: the rule is a patch however principled its predicate reads. The fix is never a better tie-break: state what the pass must LEAVE TRUE of the object it builds, test exactly that, and let a fixpoint settle which candidate goes - the pick stops mattering, and the cascade is bounded by the rounds the loop already has. THIS COSTS ONE RUN, the cheapest refutation in this file.
- A PROBLEM SOMEONE ELSE HAS SOLVED IS READ, NOT RE-DERIVED. Where an implementation of the same problem is on the machine or in the repository's history - a comparator's source, a prior branch, a deleted operator - READ IT BEFORE DESIGNING A MECHANISM: its SOURCE, not only its output. Output shows what it PRODUCED, at a full run per question and often ambiguously; source shows in minutes what it DOES - the bound, the order of operations, the arity split and the fallback no output can show. Refuting a form on a question an available source already answers is the most expensive avoidable error this file knows. What the source says is recorded ONCE as a decision naming the file and line, so the next session reads the decision, not the source.
- THE CONFIGURATION SPACE IS ENUMERATED, NOT DISCOVERED. Work on a class of defects states that class's configuration space in the plan as a product of named parameters - written as it becomes known, not demanded before anything may begin - and the milestone owns a GENERATED catalogue of fixtures over that product, run as ONE table; the gate is the table, never hand-built cases one at a time. A defect found on a case adds a ROW, not a case; a parameter the catalogue lacks is the finding. A candidate is SCREENED on the rows its own mechanism can reach, which is a reading, never a verdict.
- VERIFICATION IS PROPORTIONATE TO WHAT THE CHANGE CAN REACH, AND THE FULL TABLE GATES THE MILESTONE AND NOT EVERY STEP. A step's row states its BLAST RADIUS, the diff proves it, and that radius - never habit - sets what the step pays at its close. A step that writes no shipped output verifies THAT it wrote none, plus the rows its own mechanism reaches. A step changing one mechanism verifies that mechanism's population and the regression floor. Only a step changing shipped output on a population it cannot bound owes the whole table. THE FULL TABLE, THE FULL REGRESSION FLOOR AND THE EXPENSIVE END-TO-END CASES RUN ONCE AT THE MILESTONE'S CLOSE and at a phase's gate - not per step, never per form. A run whose result could change no verdict buys nothing, and run per step it multiplies a milestone's cost by its step count - reliably the largest removable cost in an iterating session.
- EVERY DETERMINISTIC ASSIGNMENT HAS A CONTINUOUS FALLBACK. Where a target is unreachable under a validity guard, the next step is the mechanism that relaxes the surrounding state, never another priority. The same assignment rewritten three times signals that the vocabulary is wrong: the plan replaces the priorities with a stated objective or a solver and a decision says so.
- THE BAR AND THE COST ARE STATED BEFORE THE BUILD, AND THE BAR IS RANKED. Each step's row states what accepts or refuses it and the cost per unit of work it may add, before a line is written. A BAR IS NEVER FLAT: name the ONE class that is strict - the invariant nothing may break - and put every quantity below it in a band or an aggregate. "No number worse" or "every row improves" over a many-objective measurement is not rigour: it favours candidates too timid to reach the defect and refuses one that lifts most of the table for a fraction of a percent on a row nobody ranked. A candidate is measured ONCE against that bar FOR A VERDICT, screening aside; a session iterating forms records ONE telemetry artefact for the sweep and one decision per refuted form, and stops at the THIRD FORM THAT DID NOT IMPROVE ON THE ONE BEFORE IT to restate the mechanism - three forms converging is convergence and continues; three forms trading one failure for another is thrashing, and the vocabulary is wrong.
- A BAR, CONCRETELY. Refused: *"no number worse across the catalogue."* Written instead: *"strict - nothing the contract guarantees may break; the objective improves on the cases the mechanism actually reaches; every other measured quantity moves inside a stated band, with an attribution."* Same rigour, one class strict, the rest ranked.
- DIAGNOSTICS LIVE IN SCRIPTS. Trace flags, probes and one-off prints are removed from shipped code before a step lands; a probe worth repeating is indexed in `dev/scripts/`.
- CEREMONY IS BUDGETED. A decision is recorded where a rule changes or a mechanism is refused, never per probe; finalised cases and expensive baselines are re-measured ONCE, at the MILESTONE's close; the exact resumption in `activeContext.md` is one action, not a narrative.

## Reporting to the user

The vault is what the next SESSION reads; a report is what the PERSON reads to decide what happens next - not the same document. Lead with what changed, then what it means, then what is next, briefly, in the project's own vocabulary.

- **WHAT WAS DONE** - the change itself, in a sentence or two.
- **WHAT IT MEANS** - movement against the phase's own exit criterion, as a number that moved. WHERE NOTHING THE USER IS WAITING FOR MOVED, SAY SO IN ONE LINE and say what would move it; a correct, gated step worth landing may move no acceptance clause, and calling it progress loses the phase's real position.
- **WHAT IS NEXT** - the one next action, plus anything only the user can decide.

REFUTATIONS ARE RECORDED, NOT RECOUNTED. A refuted form, a withdrawn step, a failed bar belong in `decisions.md` and the telemetry artefact, where they stop the next session repeating them. A report names one only where the user's next decision turns on it; dwelling on what failed makes an on-track phase read as in trouble and buries the line the user needed. THIS IS A CHANGE OF EMPHASIS AND NEVER OF RIGOUR: nothing is hidden or softened, no result is overstated, and a failure the user must act on is the FIRST line, not the last.

## Landing work

**WORK THAT IS NOT PUSHED IS NOT LANDED.** A step ends as a commit of its CODE on the working branch AND a push to that branch's upstream, in one act, followed by `sync`, which commits and pushes the vault records it touched: `COMMITTING` is not finished until the remote carries it. Commit and push AT EACH LANDED STEP, never in one batch at session end - unpushed code gives another session nothing to build on, and a `HEAD` in `activeContext.md` that no remote carries is a citation that cannot be followed. A branch with no upstream is given one when its first step lands, not later.

A PUSH THAT FAILS IS A FACT OF THE VAULT, NOT A DETAIL TO RETRY IN SILENCE. Rejected, unauthenticated, protected, no remote: the commit stands, `activeContext.md` takes `STATE: BLOCKED` with the failure and what was attempted, and the user is told in the session, not at its end. `resume` prints the count of unpushed commits, so a cold session sees at once what the last one left behind.

Commit authorship and any attribution trailer follow the repository's own convention and the environment's instructions; this file does not set them.

## Interface

Run from any checkout; `<skill-dir>` is the directory containing this file.

```text
<skill-dir>/scripts/xcalibre-dev doctor
<skill-dir>/scripts/xcalibre-dev init [--feature <slug> [--branch <name>]] [--remote [--name <repo>] [--owner <account>]] [repository]
<skill-dir>/scripts/xcalibre-dev sync [-m <message>] [repository]
<skill-dir>/scripts/xcalibre-dev plan <milestone-id> <slug> [--feature <slug>] [repository]
<skill-dir>/scripts/xcalibre-dev resume [--full] [--feature <slug>] [repository]
<skill-dir>/scripts/xcalibre-dev check [--feature <slug>] [repository]
<skill-dir>/scripts/xcalibre-dev migrate [repository]
<skill-dir>/scripts/xcalibre-dev migrate --apply [repository]
```

`init` scaffolds a vault from `<skill-dir>/reference/`, never overwrites an existing record, makes `dev/` its own repository and excludes it from the project; `--remote` links it to a private `<owner>/<project>-dev-vault`, creating or cloning it. `sync` commits the vault, rebases it on its remote - features built on other machines touch other folders - and pushes. `doctor` reports missing tools with install commands. `--feature <slug>` makes `init` scaffold that feature's own vault and index row; on `plan` and `resume` it defaults to the open feature bound to the checked-out branch. `plan` creates a milestone plan under the one legal name. `resume` emits Git facts, then the two records a session must have READ BEFORE IT ACTS - `activeContext.md`, which says what to do next, and `gotchas.md`, which says how work is done here: the evidence ladder, the cheapest artefact that answers a question, what a gate is and is not for. The other `LOAD` records are consulted on demand and are manifested by name and size; `--full` emits every one of them as a context packet. `check` validates that no vault file is tracked by Git, the schema, header, paths, budgets and block form, telemetry headers, the `spec.md` and `decisions.md` entry formats, and the phase/milestone/plan naming above. IT IS A LOOP AND NOT A FINAL EXAM: run it, fix exactly what it names, run it again, and only then commit the code. It exits non-zero on INVALID, so `check && commit` is safe - but a PIPELINE's status is its LAST command's, so a status read through `| tail` is that tool's and says nothing about the vault. `migrate` is dry-run by default; `--apply` renames legacy core files, converts flat JSON baselines, and archives legacy `phase*.md` fragments while preserving linked milestone plans.

## Maintaining this skill

A helper belongs in the repository unless it is project-, domain- and language-neutral. The canonical copy is this skill inside the packaged repository. Marketplace installations must not be edited or synchronised directly. **Before and after any edit: read [reference/maintaining-the-skill.md](reference/maintaining-the-skill.md).**

Source comments do not carry transient vault step or decision IDs.
