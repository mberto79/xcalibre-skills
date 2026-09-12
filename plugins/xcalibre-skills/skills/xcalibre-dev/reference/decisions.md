# decisions - current phase

Append-only. One entry per decision, at most THREE LINES, newest last:

`- <YYYY-MM-DD> D<N> <what was decided> - why: <the fact that decided it>`

`D<N>` increases by one and is never reused; it restarts at D1 each phase. Evidence is CITED, never inlined: `dev/telemetry/`, a commit SHA, a script, a requirement ID. A refused approach keeps the one number that killed it. Read this file by search, not by reading. At phase close these entries move to `dev/archive/phases/<phase>/decisions.md`.
