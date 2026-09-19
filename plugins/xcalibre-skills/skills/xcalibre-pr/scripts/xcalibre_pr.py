#!/usr/bin/env python3
"""Cross-platform preflight checks for XCALibre.jl pull requests."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def command(arguments: list[str], root: Path, capture: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            arguments,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            check=False,
        )
    except OSError as error:
        return subprocess.CompletedProcess(arguments, 127, "", str(error))


def git(root: Path, *arguments: str) -> str:
    result = command(["git", *arguments], root)
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "Git command failed").strip()
        raise RuntimeError(message)
    return result.stdout.strip()


def repository_root(path: str) -> Path:
    candidate = Path(path).resolve()
    result = command(["git", "rev-parse", "--show-toplevel"], candidate)
    if result.returncode != 0:
        raise RuntimeError(f"Not a Git repository: {candidate}")
    return Path(result.stdout.strip()).resolve()


def remote_names(root: Path) -> list[str]:
    return [name for name in git(root, "remote").splitlines() if name]


def select_remote(root: Path, requested: str | None) -> str:
    names = remote_names(root)
    if requested:
        if requested not in names:
            raise RuntimeError(f"Git remote not found: {requested}")
        return requested
    if "upstream" in names:
        return "upstream"
    if "origin" in names:
        return "origin"
    raise RuntimeError("No Git remote is configured")


def select_base(root: Path, remote: str, requested: str | None) -> str:
    if requested:
        return requested
    result = command(
        ["git", "symbolic-ref", "--quiet", "--short", f"refs/remotes/{remote}/HEAD"],
        root,
    )
    if result.returncode == 0 and result.stdout.strip().startswith(f"{remote}/"):
        return result.stdout.strip().split("/", 1)[1]
    return "main"


def github_repository(remote_url: str) -> str:
    patterns = (
        r"^https?://github\.com/([^/]+/[^/]+?)(?:\.git)?$",
        r"^git@github\.com:([^/]+/[^/]+?)(?:\.git)?$",
        r"^ssh://git@github\.com/([^/]+/[^/]+?)(?:\.git)?$",
    )
    for pattern in patterns:
        match = re.match(pattern, remote_url.strip())
        if match:
            return match.group(1)
    raise RuntimeError(f"Cannot infer a GitHub repository from remote URL: {remote_url}")


def github_json(
    repository: str, endpoint: str, query: dict[str, str] | None = None
) -> object:
    url = f"https://api.github.com/repos/{repository}/{endpoint}"
    if query:
        url = f"{url}?{urlencode(query)}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "xcalibre-pr-skill",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urlopen(Request(url, headers=headers), timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"GitHub API returned HTTP {error.code}") from error
    except URLError as error:
        raise RuntimeError(f"GitHub API request failed: {error.reason}") from error


def predict_number(root: Path, remote: str, repository: str | None) -> tuple[str, int]:
    target = repository or github_repository(git(root, "remote", "get-url", remote))
    entries = github_json(
        target,
        "issues",
        {"state": "all", "sort": "created", "direction": "desc", "per_page": "1"},
    )
    if not isinstance(entries, list):
        raise RuntimeError("Unexpected GitHub API response")
    latest = int(entries[0]["number"]) if entries else 0
    return target, latest + 1


def changed_files(root: Path, base_ref: str) -> list[str]:
    output = git(root, "diff", "--name-only", f"{base_ref}...HEAD")
    return [line for line in output.splitlines() if line]


def added_files(root: Path, base_ref: str) -> list[str]:
    output = git(root, "diff", "--name-only", "--diff-filter=A", f"{base_ref}...HEAD")
    return [line for line in output.splitlines() if line]


def changed_line_numbers(root: Path, base_ref: str) -> dict[str, set[int]]:
    output = git(root, "diff", "--unified=0", f"{base_ref}...HEAD", "--", "*.jl")
    changed: dict[str, set[int]] = {}
    current: str | None = None
    for line in output.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
            changed.setdefault(current, set())
        elif current and line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            if match:
                start = int(match.group(1))
                count = int(match.group(2) or "1")
                changed[current].update(range(start, start + count))
    return changed


def long_changed_comment_blocks(
    root: Path, changed: dict[str, set[int]]
) -> list[tuple[str, int, int, int]]:
    violations = []
    for relative, changed_lines in changed.items():
        path = root / relative
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        index = 0
        while index < len(lines):
            if lines[index].lstrip().startswith("#") and not (
                index == 0 and lines[index].startswith("#!")
            ):
                start = index
                last_comment = index
                comment_count = 0
                cursor = index
                while cursor < len(lines):
                    stripped = lines[cursor].strip()
                    if stripped.startswith("#"):
                        last_comment = cursor
                        comment_count += 1
                    elif stripped:
                        break
                    cursor += 1
                line_range = set(range(start + 1, last_comment + 2))
                if comment_count > 3 and changed_lines.intersection(line_range):
                    violations.append((relative, start + 1, last_comment + 1, comment_count))
                index = max(cursor, index + 1)
            else:
                index += 1
    return violations


def added_docstring_locations(root: Path, changed: dict[str, set[int]]) -> list[str]:
    locations = []
    for relative, line_numbers in changed.items():
        path = root / relative
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_number in sorted(line_numbers):
            if line_number <= len(lines) and '"""' in lines[line_number - 1]:
                locations.append(f"{relative}:{line_number}")
    return locations


def dependency_names(text: str) -> set[str]:
    names: set[str] = set()
    in_dependencies = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_dependencies = stripped in {"[deps]", "[weakdeps]", "[extras]"}
        elif in_dependencies:
            match = re.match(r"([A-Za-z][A-Za-z0-9_]*)\s*=", stripped)
            if match:
                names.add(match.group(1))
    return names


def added_dependencies(root: Path, base_ref: str) -> list[str]:
    project = root / "Project.toml"
    if not project.is_file():
        return []
    current = dependency_names(project.read_text(encoding="utf-8"))
    previous = command(["git", "show", f"{base_ref}:Project.toml"], root)
    base = dependency_names(previous.stdout) if previous.returncode == 0 else set()
    return sorted(current - base)


def pull_request_description(
    root: Path,
    remote: str,
    repository: str | None,
    number: int | None,
    description_file: str | None,
) -> tuple[str, str, str | None] | None:
    if number is not None:
        target = repository or github_repository(git(root, "remote", "get-url", remote))
        response = github_json(target, f"pulls/{number}")
        if not isinstance(response, dict):
            raise RuntimeError("Unexpected GitHub pull-request response")
        user = response.get("user")
        author = user.get("login") if isinstance(user, dict) else None
        return f"{target}#{number}", str(response.get("body") or "").strip(), str(author or "")
    if description_file:
        path = Path(description_file)
        if not path.is_absolute():
            path = root / path
        if not path.is_file():
            raise RuntimeError(f"PR description file not found: {path}")
        return str(path), path.read_text(encoding="utf-8").strip(), None
    return None


def authenticated_github_user(root: Path) -> str | None:
    response = command(["gh", "api", "user", "--jq", ".login"], root)
    return response.stdout.strip() if response.returncode == 0 and response.stdout.strip() else None


def ai_disclosure(body: str) -> str | None:
    match = re.search(r"(?im)^\s*(?:[-*]\s*)?AI assistance:\s*(\S.*)\s*$", body)
    return match.group(1).strip() if match else None


def changelog_lines(path: Path, number: int) -> list[tuple[int, str]]:
    marker = re.compile(rf"\[#{number}\](?:\(@ref\))?")
    matches = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if marker.search(line):
            matches.append((line_number, line.strip()))
    return matches


def result(label: str, status: str, detail: str) -> bool:
    print(f"[{status}] {label}: {detail}")
    return status == "PASS"


def print_number(arguments: argparse.Namespace) -> int:
    try:
        root = repository_root(arguments.repository)
        remote = select_remote(root, arguments.remote)
        target, number = predict_number(root, remote, arguments.github_repository)
    except RuntimeError as error:
        print(f"[FAIL] PR number: {error}", file=sys.stderr)
        return 1
    print(f"repository={target}")
    print(f"predicted_number={number}")
    print("provisional=true")
    print("note=GitHub issues and pull requests share one sequence; this number is not reserved.")
    return 0


def preflight(arguments: argparse.Namespace) -> int:
    failures = 0
    reviews = 0
    open_items: list[str] = []
    confirmed = set(arguments.confirm)
    if "all" in confirmed:
        confirmed.update(
            {"theme", "description", "documentation", "example", "docstrings", "dependencies", "propagation", "grids", "identity"}
        )

    def record(label: str, status: str, detail: str) -> None:
        nonlocal failures, reviews
        result(label, status, detail)
        if status == "FAIL":
            failures += 1
            open_items.append(f"{label}: {detail}")
        elif status in {"REVIEW", "SKIP"}:
            reviews += 1
            open_items.append(f"{label}: {detail}")

    def review(key: str, label: str, detail: str) -> None:
        record(label, "PASS" if key in confirmed else "REVIEW", detail)

    try:
        root = repository_root(arguments.repository)
        remote = select_remote(root, arguments.remote)
        base = select_base(root, remote, arguments.base)
        branch = git(root, "branch", "--show-current")
    except RuntimeError as error:
        print(f"[FAIL] Repository: {error}", file=sys.stderr)
        print("open_items:")
        print(f"  - Repository: {error}")
        print("[REMINDER] Confirm whether the pull request has already been discussed with the development team.")
        return 1

    if not branch:
        record("Feature branch", "FAIL", "detached HEAD")
    elif branch == base:
        record("Feature branch", "FAIL", f"current branch is the base branch {base}")
    else:
        record("Feature branch", "PASS", branch)

    if not arguments.no_fetch:
        fetched = command(["git", "fetch", "--quiet", remote], root)
        if fetched.returncode != 0:
            detail = (fetched.stderr or fetched.stdout or "fetch failed").strip()
            record("Fetch", "FAIL", detail)
    base_ref = f"{remote}/{base}"
    try:
        behind_text, ahead_text = git(
            root, "rev-list", "--left-right", "--count", f"{base_ref}...HEAD"
        ).split()
        behind, ahead = int(behind_text), int(ahead_text)
        status = "PASS" if behind == 0 else "FAIL"
        record("Base synchronisation", status, f"behind={behind}, ahead={ahead}, base={base_ref}")
    except (RuntimeError, ValueError) as error:
        record("Base synchronisation", "FAIL", str(error))

    tracking = command(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], root
    )
    if tracking.returncode != 0:
        record("Remote branch", "FAIL", "no upstream tracking branch")
    else:
        tracking_ref = tracking.stdout.strip()
        tracking_remote = tracking_ref.split("/", 1)[0]
        if not arguments.no_fetch and tracking_remote != remote:
            fetched = command(["git", "fetch", "--quiet", tracking_remote], root)
            if fetched.returncode != 0:
                detail = (fetched.stderr or fetched.stdout or "fetch failed").strip()
                record("Feature remote fetch", "FAIL", detail)
        try:
            remote_only, local_only = map(
                int,
                git(root, "rev-list", "--left-right", "--count", f"{tracking_ref}...HEAD").split(),
            )
            status = "PASS" if remote_only == 0 and local_only == 0 else "FAIL"
            record(
                "Remote branch",
                status,
                f"remote_only={remote_only}, local_only={local_only}, upstream={tracking_ref}",
            )
        except (RuntimeError, ValueError) as error:
            record("Remote branch", "FAIL", str(error))

    try:
        files = changed_files(root, base_ref)
        new_files = added_files(root, base_ref)
        changed_lines = changed_line_numbers(root, base_ref)
        commits = git(root, "log", "--format=%s", f"{base_ref}..HEAD").splitlines()
        review("theme", "Single theme", "confirm that all listed changes serve one coherent purpose")
        print("  commits:")
        for subject in commits:
            print(f"    - {subject}")
        print("  files:")
        for path in files:
            print(f"    - {path}")
        vault_files = [path for path in files if path == "dev" or path.startswith("dev/")]
        if vault_files:
            record(
                "Development vault",
                "FAIL",
                f"{len(vault_files)} file(s) under dev/ differ from {base_ref}; untrack them with "
                "`git rm -r --cached dev`, commit, and keep dev/ in .git/info/exclude",
            )
        else:
            record("Development vault", "PASS", "no dev/ files in the pull request")
    except RuntimeError as error:
        record("Change inspection", "FAIL", str(error))
        files = []
        new_files = []
        changed_lines = {}

    actual_number = arguments.pr_number
    number = actual_number
    if number is None:
        try:
            target, number = predict_number(root, remote, arguments.github_repository)
            record("PR number", "REVIEW", f"predicted #{number} for {target}; not reserved")
        except RuntimeError as error:
            record("PR number", "FAIL", str(error))

    changelog = root / arguments.changelog
    if number is not None:
        if not changelog.is_file():
            record("Changelog", "FAIL", f"file not found: {changelog}")
        else:
            lines = changelog_lines(changelog, number)
            if lines:
                record("Changelog", "PASS", f"{len(lines)} item(s) reference #{number}")
                for line_number, text in lines:
                    print(f"  {arguments.changelog}:{line_number}: {text}")
            else:
                record("Changelog", "FAIL", f"no item references #{number}")

    description_body = ""
    pr_author: str | None = None
    try:
        description = pull_request_description(
            root,
            remote,
            arguments.github_repository,
            actual_number,
            arguments.description_file,
        )
        if description is None:
            record("PR description", "FAIL", "provide --description-file or an assigned --pr-number")
        elif not description[1]:
            record("PR description", "FAIL", f"empty description at {description[0]}")
        else:
            description_body = description[1]
            pr_author = description[2]
            review(
                "description",
                "PR description",
                f"confirm {description[0]} clearly explains what was added or changed",
            )
    except RuntimeError as error:
        record("PR description", "FAIL", str(error))

    if not arguments.expected_author:
        record("PR author", "FAIL", "provide the contributor's GitHub login with --expected-author")
    elif actual_number is not None:
        if not pr_author:
            record("PR author", "FAIL", "could not read the pull-request author from GitHub")
        elif pr_author.casefold() == arguments.expected_author.casefold():
            record("PR author", "PASS", f"opened by {pr_author}")
        else:
            record(
                "PR author",
                "FAIL",
                f"opened by {pr_author}; expected the user's account {arguments.expected_author}",
            )
    else:
        authenticated = authenticated_github_user(root)
        if authenticated and authenticated.casefold() == arguments.expected_author.casefold():
            record("GitHub identity", "PASS", f"authenticated as {authenticated}")
        elif authenticated:
            record(
                "GitHub identity",
                "FAIL",
                f"authenticated as {authenticated}; expected {arguments.expected_author}",
            )
        else:
            review(
                "identity",
                "GitHub identity",
                f"confirm the PR will be opened by the user's account {arguments.expected_author}",
            )

    if not arguments.ai_vendor or not arguments.ai_model:
        record("AI disclosure", "FAIL", "provide both --ai-vendor and --ai-model")
    elif not description_body:
        record("AI disclosure", "FAIL", "a PR description is required before disclosure can be checked")
    else:
        disclosure = ai_disclosure(description_body)
        expected = f"AI assistance: {arguments.ai_vendor}, {arguments.ai_model}."
        if (
            disclosure
            and arguments.ai_vendor.casefold() in disclosure.casefold()
            and arguments.ai_model.casefold() in disclosure.casefold()
        ):
            record("AI disclosure", "PASS", expected)
        else:
            record("AI disclosure", "FAIL", f"add this one-line note to the PR description: {expected}")

    if arguments.feature:
        test_paths = [path for path in files if Path(path).parts[0].lower() in {"test", "tests"}]
        documentation_paths = [
            path
            for path in files
            if Path(path).parts[0].lower() in {"doc", "docs"}
            or Path(path).name.lower().startswith("readme")
        ]
        example_paths = [
            path for path in files if Path(path).parts[0].lower() in {"example", "examples"}
        ]
        record("Feature tests", "PASS" if test_paths else "FAIL", ", ".join(test_paths) or "none")
        record(
            "Feature documentation",
            "PASS" if documentation_paths else "FAIL",
            ", ".join(documentation_paths) or "none",
        )
        if documentation_paths:
            review(
                "documentation",
                "Documentation convention",
                "confirm the feature documentation follows the existing project convention",
            )
        record("Minimal example", "PASS" if example_paths else "FAIL", ", ".join(example_paths) or "none")
        if example_paths:
            review(
                "example",
                "Example quality",
                "confirm the example is minimal and uses an existing grid where practical",
            )

        grid_suffixes = {".cgns", ".foam", ".msh", ".obj", ".stl", ".unv", ".vtk", ".vtu"}
        new_grids = [path for path in new_files if Path(path).suffix.lower() in grid_suffixes]
        if new_grids:
            details = []
            for relative in new_grids:
                path = root / relative
                size = path.stat().st_size if path.is_file() else 0
                details.append(f"{relative} ({size} bytes)")
            review(
                "grids",
                "New example grids",
                "confirm each new grid is necessary and very small: " + ", ".join(details),
            )
        else:
            record("New example grids", "PASS", "no new grid files detected")

        code_paths = [path for path in files if Path(path).suffix.lower() == ".jl"]
        if code_paths:
            docstrings = added_docstring_locations(root, changed_lines)
            detail = ", ".join(docstrings) if docstrings else "no added docstring delimiters detected"
            review(
                "docstrings",
                "User API docstrings",
                f"confirm docstrings are limited to user-level API functions; {detail}",
            )

    comment_violations = long_changed_comment_blocks(root, changed_lines)
    if comment_violations:
        detail = ", ".join(
            f"{path}:{start}-{end} ({count} comment lines)"
            for path, start, end, count in comment_violations
        )
        record("Comment length", "FAIL", detail)
    else:
        record("Comment length", "PASS", "no changed comment block exceeds three lines")

    dependencies = added_dependencies(root, base_ref)
    if dependencies:
        review(
            "dependencies",
            "Added dependencies",
            "confirm each dependency and its licence are explicitly listed in the PR description: "
            + ", ".join(dependencies),
        )
    else:
        record("Added dependencies", "PASS", "none")

    if any(Path(path).suffix.lower() == ".jl" for path in files):
        review(
            "propagation",
            "Common function propagation",
            "confirm changes to common or base functions are propagated to every affected caller, test, and document",
        )

    if arguments.skip_tests:
        record("Package tests", "SKIP", "explicitly skipped")
    else:
        print("[RUN] Package tests: julia --project=. -e 'using Pkg; Pkg.test()'")
        tested = command(
            ["julia", "--project=.", "-e", "using Pkg; Pkg.test()"], root, capture=False
        )
        if tested.returncode == 0:
            record("Package tests", "PASS", "completed successfully")
        else:
            record("Package tests", "FAIL", f"exit code {tested.returncode}")

    print("[REMINDER] Confirm whether the pull request has already been discussed with the development team.")
    if open_items:
        print("open_items:")
        for item in open_items:
            print(f"  - {item}")
    summary = "FAIL" if failures else "REVIEW" if reviews else "PASS"
    print(f"summary={summary} failures={failures} reviews={reviews}")
    return 1 if failures else 2 if reviews else 0


def parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--repository", default=".", help="path inside the Git checkout")
    shared.add_argument("--remote", help="base remote; defaults to upstream, then origin")
    shared.add_argument("--github-repository", help="GitHub owner/name when it cannot be inferred")

    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)

    number = subcommands.add_parser("next-number", parents=[shared])
    number.set_defaults(handler=print_number)

    check = subcommands.add_parser("preflight", parents=[shared])
    check.add_argument("--base", help="base branch; defaults to the remote default or main")
    check.add_argument("--no-fetch", action="store_true", help="use existing remote-tracking refs")
    check.add_argument("--pr-number", type=int, help="actual assigned pull-request number")
    check.add_argument("--description-file", help="draft PR description relative to the repository")
    check.add_argument("--expected-author", help="GitHub login of the human contributor")
    check.add_argument("--ai-vendor", help="AI vendor disclosed in the PR description")
    check.add_argument("--ai-model", help="AI model disclosed in the PR description")
    check.add_argument("--changelog", default="CHANGELOG.md")
    check.add_argument("--feature", action="store_true", help="require changed tests and documentation")
    check.add_argument(
        "--confirm",
        action="append",
        default=[],
        choices=("theme", "description", "documentation", "example", "docstrings", "dependencies", "propagation", "grids", "identity", "all"),
        help="record a completed judgement-based review; repeat as needed",
    )
    check.add_argument("--skip-tests", action="store_true", help="skip the local Julia package test")
    check.set_defaults(handler=preflight)
    return root


def main() -> int:
    arguments = parser().parse_args()
    return arguments.handler(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
