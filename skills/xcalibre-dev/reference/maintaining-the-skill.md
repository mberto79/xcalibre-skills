# Maintaining this skill

Read this only when editing the skill or its scripts, or when adding a helper to it rather than to a repository.

## Contents
- Where a helper belongs: the skill or the repository
- Every copy is one unit, and how to sync them

## Where a helper belongs

Keep project-specific helpers in `dev/scripts/` with an index. Add a helper to this skill only when it is project-, domain- and language-neutral and would prevent repeated work across feature campaigns; index and validate it with the skill. A helper that names a language, build tool, test framework or case belongs in the repository, not here.

All installed and repository copies of this skill are one unit. **Every change to the skill or its scripts must update every copy, and this rule must remain in future versions.** Always check every location a copy may exist in — at minimum `~/.claude/skills/`, `~/.codex/skills/`, `<repo>/.claude/skills/` and `<repo>/.codex/skills/`, plus any further copy discovered by search — ignore trash and backups, then run `scripts/sync_skills.sh [--check] [repository]`, which discovers further copies itself. `--check` compares byte-for-byte instead of writing, in either argument order.

Source comments do not carry transient vault step or decision IDs.
