# <project> — requirements

WHAT THE DELIVERED PRODUCT MUST BE TRUE OF. One test admits a clause here: could a completely different implementation satisfy it? If not, it is not a requirement. Mechanisms, names and call order are `dev/architecture.md`; how to build, run, gate and measure is `dev/gotchas.md`; why a mechanism was chosen or refused is `dev/decisions.md`. Requirement IDs are permanent — text is amended under its existing ID and repeals are recorded in place.

This file is a record for people of what the product promises, not an instruction set for agents. Name the BINDING CORE — the few clauses that define the product and that no session relaxes — in one line here; every other clause is AMENDABLE by a session holding better evidence, under its own ID, with a decision saying why. A candidate is never refused for departing from an amendable clause or from `dev/architecture.md`; it is measured. No clause names a mechanism, an owner, a milestone, a date or a ruling: those live in the other records.

## goal

One paragraph: what the product is for, and the one property that outranks convenience.

## vocabulary

- **<term>** — the definition every record uses. Define a term once, here.

## priority

The ranking used when two clauses conflict, worst-first, and the rule for reading a verdict across several numbers at once.

## quality bars

- **Q1 <name>** — the property and its numeric bar.

## requirements

One line each where possible, four at most:

`<ID> <WHAT IT ENFORCES, IN CAPITALS> — <what must be true, briefly>.`

The ID is permanent. The capitalised clause is what the requirement enforces, so the list can be scanned. The statement is an OUTCOME: it never names a keyword, function, file, constant or stage order — that is documentation, and documentation is not a requirement. Anything needing more than four lines is architecture, method or a decision, and goes to those records.

R1 <WHAT IT ENFORCES> — <what must be true of the delivered product>.
R2 <WHAT IT ENFORCES> — <...>.

## acceptance

A phase closes when all of the following hold on the artifacts named here.

1. **<clause>** — <what is measured and against what>.

A clause here is amended, replaced or added by a decision that names what changed and why; the list is never frozen.

## deliberately NOT requirements

What has been considered and is out of scope, so it is not re-proposed.

## repealed

Requirement IDs that no longer bind, each naming what replaced it and where the evidence is.
