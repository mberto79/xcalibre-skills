#!/usr/bin/env python3
"""Light-touch development journal: dev/STATUS.md, dev/journal.md and dev/runs.jsonl."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATUS_MAX_LINES = 40
JOURNAL_MAX_LINES = 300
RUNS_MAX_LINES = 2000
LEGACY = ("activeContext.md", "decisions.md", "phaseRoadmap.md", "roadmap.md", "spec.md", "SCHEMA.md")

STATUS_TEMPLATE = """# Status

## Goal

## Branch

## Now

## Next

## Questions for the user

## Running agents and jobs
"""


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def repository_root(path: str) -> Path:
    start = Path(path).resolve()
    top = git(start, "rev-parse", "--show-toplevel")
    return Path(top) if top else start


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def position(root: Path) -> str:
    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD") or "no-branch"
    sha = git(root, "rev-parse", "--short", "HEAD") or "no-commit"
    return f"{branch}@{sha}"


def line_count(path: Path) -> int:
    if not path.is_file():
        return 0
    with path.open(encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def append(path: Path, text: str, limit: int) -> None:
    # Full files move to dev/archive/ so the live file stays cheap to read.
    if line_count(path) >= limit:
        archive = path.parent / "archive"
        archive.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        path.rename(archive / f"{path.stem}-{stamp}{path.suffix}")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text.rstrip("\n") + "\n")


def tail(path: Path, count: int) -> list[str]:
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()[-count:]


def ensure_excluded(root: Path) -> None:
    git_dir = git(root, "rev-parse", "--git-dir")
    if not git_dir:
        return
    exclude = (root / git_dir / "info" / "exclude").resolve()
    exclude.parent.mkdir(parents=True, exist_ok=True)
    lines = exclude.read_text(encoding="utf-8").splitlines() if exclude.is_file() else []
    if "/dev/" not in lines:
        with exclude.open("a", encoding="utf-8") as handle:
            handle.write("/dev/\n")


def format_run(text: str) -> str:
    try:
        run = json.loads(text)
    except json.JSONDecodeError:
        return text
    metrics = " ".join(f"{key}={value}" for key, value in run.get("metrics", {}).items())
    parts = [run.get("t", ""), run.get("at", ""), run.get("verdict", ""), run.get("what", ""), metrics]
    return " | ".join(part for part in parts if part)


AGENT_IDENTITY = re.compile(
    r"(?i)\b(?:claude|anthropic|codex|openai|chatgpt|copilot|gemini|cursor|devin|aider)\b|\[bot\]|noreply@(?:anthropic|openai)"
)
AI_TRAILER = re.compile(r"(?im)^(?:co-authored-by:.*(?:claude|anthropic|codex|openai|copilot|gemini|\[bot\]).*|.*generated (?:with|by) .*(?:claude|codex|copilot|chatgpt|gemini|\bai\b).*)$")


def authorship_warnings(root: Path) -> list[str]:
    warnings = []
    identity = f"{git(root, 'config', 'user.name')} <{git(root, 'config', 'user.email')}>"
    if AGENT_IDENTITY.search(identity) or identity == " <>":
        warnings.append(f"Git identity is {identity}; commits must use the user's own name and email (git config user.name/user.email)")
    # Only this branch's own commits: those not on the base branch, else those not yet pushed.
    head = git(root, "rev-parse", "HEAD")
    bases = [git(root, "merge-base", "HEAD", ref) for ref in ("origin/HEAD", "origin/main", "origin/master")]
    if head in bases:
        return warnings
    base = next((b for b in bases if b), "")
    scope = f"{base}..HEAD" if base else ("@{upstream}..HEAD" if git(root, "rev-parse", "@{upstream}") else "-20")
    log = git(root, "log", scope, "--format=%h%x1f%an <%ae>%x1f%cn <%ce>%x1f%B%x1e")
    bad = []
    for entry in filter(None, (item.strip() for item in log.split("\x1e"))):
        sha, author, committer, body = (entry.split("\x1f") + ["", "", ""])[:4]
        if AGENT_IDENTITY.search(author + committer) or AI_TRAILER.search(body):
            bad.append(sha)
    if bad:
        warnings.append("commits with an agent author or AI attribution: " + ", ".join(bad[:10]) + "; ask the user before rewriting them")
    return warnings


def command_init(root: Path, _: argparse.Namespace) -> int:
    dev = root / "dev"
    dev.mkdir(exist_ok=True)
    status = dev / "STATUS.md"
    if not status.exists():
        status.write_text(STATUS_TEMPLATE, encoding="utf-8")
    for name in ("journal.md", "runs.jsonl"):
        (dev / name).touch()
    ensure_excluded(root)
    print(f"dev journal ready in {dev}; /dev/ is excluded from Git")
    for warning in authorship_warnings(root):
        print(f"WARNING: {warning}")
    return 0


def command_resume(root: Path, _: argparse.Namespace) -> int:
    dev = root / "dev"
    if not dev.is_dir():
        print("no dev/ journal here; run init")
        return 1
    dirty = git(root, "status", "--porcelain")
    unpushed = git(root, "rev-list", "--count", "@{upstream}..HEAD") or "unknown (no upstream)"
    print(f"git: {position(root)}, {len(dirty.splitlines())} uncommitted change(s), {unpushed} unpushed commit(s)")

    warnings = []
    if git(root, "ls-files", "dev"):
        warnings.append("dev/ files are tracked by Git; untrack them with `git rm -r --cached dev`")
    status = dev / "STATUS.md"
    if line_count(status) > STATUS_MAX_LINES:
        warnings.append(f"STATUS.md is over {STATUS_MAX_LINES} lines; trim it to the current state")
    warnings += authorship_warnings(root)
    legacy = [name for name in LEGACY if (dev / name).is_file()]
    if legacy:
        warnings.append("earlier vault files found (" + ", ".join(legacy) + "); fold what is live into STATUS.md, then archive them")

    print("\n== dev/STATUS.md ==")
    print(status.read_text(encoding="utf-8").strip() if status.is_file() else "(missing)")
    print("\n== last journal entries ==")
    print("\n".join(tail(dev / "journal.md", 10)) or "(none)")
    print("\n== last runs ==")
    print("\n".join(format_run(line) for line in tail(dev / "runs.jsonl", 5)) or "(none)")
    for warning in warnings:
        print(f"\nWARNING: {warning}")
    return 0


def command_log(root: Path, arguments: argparse.Namespace) -> int:
    text = " ".join(arguments.text).replace("\n", " ").strip()
    if not text:
        print("nothing to log")
        return 1
    append(root / "dev" / "journal.md", f"{now()} {position(root)} {text}", JOURNAL_MAX_LINES)
    return 0


def command_run(root: Path, arguments: argparse.Namespace) -> int:
    metrics = {}
    for item in arguments.metric:
        key, separator, value = item.partition("=")
        if not separator:
            print(f"metric must be key=value: {item}")
            return 1
        try:
            metrics[key] = json.loads(value)
        except json.JSONDecodeError:
            metrics[key] = value
    run = {"t": now(), "at": position(root), "what": arguments.what, "verdict": arguments.verdict}
    if arguments.cmd:
        run["cmd"] = arguments.cmd
    if metrics:
        run["metrics"] = metrics
    if arguments.note:
        run["note"] = arguments.note
    append(root / "dev" / "runs.jsonl", json.dumps(run, separators=(",", ":")), RUNS_MAX_LINES)
    return 0


def command_runs(root: Path, arguments: argparse.Namespace) -> int:
    lines = tail(root / "dev" / "runs.jsonl", RUNS_MAX_LINES)
    if arguments.pattern:
        lines = [line for line in lines if arguments.pattern.lower() in line.lower()]
    print("\n".join(format_run(line) for line in lines[-arguments.n:]) or "(no matching runs)")
    return 0


def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repository", default=".", help="project checkout (default: current directory)")
    main = argparse.ArgumentParser(description=__doc__)
    commands = main.add_subparsers(dest="command", required=True)
    commands.add_parser("init", parents=[common], help="create dev/ and exclude it from Git")
    commands.add_parser("resume", parents=[common], help="print Git state, status, recent journal and runs")
    log = commands.add_parser("log", parents=[common], help="append one line to the journal")
    log.add_argument("text", nargs="+")
    run = commands.add_parser("run", parents=[common], help="record one trial or measurement")
    run.add_argument("what")
    run.add_argument("--cmd")
    run.add_argument("--verdict", default="info", choices=("pass", "fail", "info"))
    run.add_argument("-m", "--metric", action="append", default=[], help="key=value; repeat as needed")
    run.add_argument("--note")
    runs = commands.add_parser("runs", parents=[common], help="list recorded runs, optionally filtered")
    runs.add_argument("pattern", nargs="?")
    runs.add_argument("-n", type=int, default=20)
    return main


def main() -> int:
    arguments = parser().parse_args()
    root = repository_root(arguments.repository)
    if arguments.command != "init" and not (root / "dev").is_dir():
        print("no dev/ journal here; run init")
        return 1
    handlers = {"init": command_init, "resume": command_resume, "log": command_log, "run": command_run, "runs": command_runs}
    return handlers[arguments.command](root, arguments)


if __name__ == "__main__":
    sys.exit(main())
