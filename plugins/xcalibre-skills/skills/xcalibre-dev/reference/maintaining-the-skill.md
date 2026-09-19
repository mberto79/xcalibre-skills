# Maintaining this skill

Read this only when editing the skill or its scripts, or when adding a helper to it rather than to a repository.

## Contents
- Where a helper belongs: the skill or the repository
- Marketplace packaging and validation

## Where a helper belongs

Keep project-specific helpers in `dev/scripts/` with an index. Add a helper to this skill only when it is project-, domain- and language-neutral and would prevent repeated work across feature campaigns; index and validate it with the skill. A helper that names a language, build tool, test framework or case belongs in the repository, not here.

The repository copy under `plugins/xcalibre-skills/skills/xcalibre-dev/` is canonical. Claude and Codex installations come from their marketplace manifests; never synchronise or edit installed copies directly.

After changing this skill or its scripts, validate the canonical skill and both plugin manifests. Commit and push the change so marketplace users receive the revised package through their platform's update mechanism.

Source comments do not carry transient vault step or decision IDs.
