---
name: xcalibre-dev
description: Run an XCALibre.jl development session that can be resumed after a crash — sets up the branch and a small journal, keeps a 50-minute progress check, and keeps records small. Use when the user starts, resumes or continues a feature, refactor or debugging effort in XCALibre.jl ("I'm starting a new feature…", "pick up where we left off"). Not for questions or one-off edits.
---

# XCALibre Dev Journal

Three small files under `dev/` record where a development session is and what it has done. They let a new session pick up after a crash and let a human audit the work. This skill records work; it does not prescribe how to do it. The user's instructions, the host's system prompt and your own judgement come first.

## Files

`dev/` sits in the project checkout and never enters a commit or pull request: `init` adds `/dev/` to `.git/info/exclude`, and `xcalibre-pr` fails if a `dev/` file is tracked.

| File | Holds | Written by | Size |
|---|---|---|---|
| `dev/STATUS.md` | Where the work is now | editing it in place | at most 40 lines |
| `dev/journal.md` | What happened, in order | `log`, one line per entry | rotated at 300 lines |
| `dev/runs.jsonl` | Trials and measurements | `run`, one JSON object per line | rotated at 2000 lines |

- **`STATUS.md`** has six short sections: Goal, Branch, Now, Next (the exact next action), Questions for the user, and Running agents and jobs. Overwrite it as things change; history belongs in the journal.
- **`journal.md`** lines read `<UTC time> <branch>@<sha> <one sentence>`. Log what a later reader needs: a direction chosen, an idea refuted with the number that refuted it, a commit landed, a blocker. Do not log routine commands.
- **`runs.jsonl`** keeps the numbers from a trial, not its output: what was tried, the command, metrics as `key=value`, and a verdict. Query it with `runs <pattern>` or `jq`. Raw logs are not kept; once the numbers are recorded, delete the log.

Rotation moves a full file to `dev/archive/` and starts a fresh one. Nothing else is required. Keep a file that will be used again, such as a benchmark script or a small fixture, under `dev/scripts/` with a one-line note in `STATUS.md`. Do not keep logs, dumps or one-off output.

## Starting and resuming

When the user says they are starting something ("I'm starting a new feature that…"):

1. If the checkout is on the base branch, update it and create a feature branch with a short descriptive name.
2. Run `init`, write the request into Goal in `STATUS.md`, and add a first `log` line.
3. Start the 50-minute check (below), then get on with the work.

When the user asks to resume, or a session starts with a `dev/` already present, run `resume`, read what it prints, restart the 50-minute check and continue from Next.

## When to write

- **After a meaningful step:** add a `log` line, add a `run` for any measurement, and update `STATUS.md` if Now or Next changed.
- **Before stopping, or when the context is getting long:** make sure Next in `STATUS.md` is exact enough for a cold session to act on.

## 50-minute check

At the start of a session, schedule a recurring check every 50 minutes with whatever the host provides, for example `/loop 50m` in Claude Code. At each check:

1. Bring `STATUS.md` up to date, and add a journal line if anything moved.
2. Ask every running agent or background job for a one-line progress update. List them under Running agents and jobs, and redirect or stop any that are stuck.
3. If nothing has moved since the last check, tell the user in one line.

Cancel the check when the session's work ends. Without a scheduler, run the check at natural breaks.

## Earlier vaults

If `resume` finds files from the earlier vault format (`activeContext.md`, `decisions.md` and others), read them once, carry anything still live into `STATUS.md`, then move them to `dev/archive/`.

`dev/` lives only on this machine. To keep it if the machine is lost, the user can make `dev/` its own Git repository with a private remote; this skill does not manage that.

## Interface

`<skill-dir>` is the directory containing this file. Every command takes `--repository <path>`, defaulting to the current directory.

```text
python <skill-dir>/scripts/devlog.py init
python <skill-dir>/scripts/devlog.py resume
python <skill-dir>/scripts/devlog.py log "<one sentence>"
python <skill-dir>/scripts/devlog.py run "<what>" [--cmd "<command>"] [--verdict pass|fail|info] [-m key=value ...] [--note "<text>"]
python <skill-dir>/scripts/devlog.py runs [<pattern>] [-n <count>]
```

`resume` prints the Git state (branch, commit, uncommitted changes, unpushed commits), `STATUS.md`, the last ten journal lines and the last five runs, and warns when a file is over its size or `dev/` is tracked by Git.
