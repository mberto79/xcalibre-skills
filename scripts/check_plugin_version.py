#!/usr/bin/env python3
"""Check the plugin version in the Claude and Codex manifests.

Usage:
    python3 scripts/check_plugin_version.py [BASE_REF]

Always checks that both manifests carry the same valid SemVer 2.0.0 version.
With BASE_REF (for example origin/main), it also checks that the version is
higher than on BASE_REF whenever anything under plugins/ has changed.
"""

import json
import re
import subprocess
import sys

MANIFESTS = (
    "plugins/xcalibre-skills/.claude-plugin/plugin.json",
    "plugins/xcalibre-skills/.codex-plugin/plugin.json",
)

# Official SemVer 2.0.0 pattern from https://semver.org.
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def precedence_key(version):
    """Sort key following SemVer 2.0.0 precedence; build metadata is ignored."""
    major, minor, patch, pre, _ = SEMVER.match(version).groups()
    if pre is None:
        pre_key = (1,)
    else:
        pre_key = (0,) + tuple(
            (0, int(part), "") if part.isdigit() else (1, 0, part)
            for part in pre.split(".")
        )
    return (int(major), int(minor), int(patch)) + (pre_key,)


def git(*args):
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def main():
    errors = []
    versions = {}
    for path in MANIFESTS:
        with open(path, encoding="utf-8") as handle:
            version = json.load(handle).get("version")
        versions[path] = version
        if not isinstance(version, str) or not SEMVER.match(version):
            errors.append(f"{path}: version {version!r} is not SemVer 2.0.0")

    if len(set(versions.values())) != 1:
        listed = ", ".join(f"{p} = {v}" for p, v in versions.items())
        errors.append(f"manifest versions differ: {listed}")

    if not errors and len(sys.argv) > 1:
        base = sys.argv[1]
        version = versions[MANIFESTS[0]]
        changed = git("diff", "--name-only", f"{base}...HEAD", "--", "plugins/")
        if changed.strip():
            base_version = json.loads(git("show", f"{base}:{MANIFESTS[1]}")).get(
                "version", "0.0.0"
            )
            if precedence_key(version) <= precedence_key(base_version):
                errors.append(
                    f"plugins/ changed but version {version} is not higher than "
                    f"{base_version} on {base}; bump it in both manifests"
                )

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"plugin version {versions[MANIFESTS[0]]} OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
