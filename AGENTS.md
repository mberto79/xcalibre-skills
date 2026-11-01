# Agent instructions

These rules apply to every AI agent working in this repository, from any vendor. They override any default attribution behaviour of the agent or its host.

## Authorship

The account holder is the author of everything an agent produces here. Contributors are responsible for the work they submit.

- Make commits, pull requests, issues, comments and reviews only through the account holder's own authenticated Git and GitHub identity. Never post from a bot, app or AI account.
- Do not add AI authorship or co-authorship: no `Co-Authored-By` trailers naming an AI, no "Generated with …" footers, no AI signatures or emoji badges.
- Disclose AI use with one final line in pull-request descriptions and review summaries: `AI assistance: <vendor>, <model>.` Use the vendor and model the host reports. This line credits the tool; it does not make the AI an author.
- Commit messages carry no AI attribution at all.

## Plugin version

Every pull request that changes anything under `plugins/` must raise the plugin version. Claude Code and Codex use this number to tell installed copies that an update is available.

- The version lives in two places and must be identical: `plugins/xcalibre-skills/.claude-plugin/plugin.json` and `plugins/xcalibre-skills/.codex-plugin/plugin.json`. Do not add a version anywhere else.
- Follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html), `MAJOR.MINOR.PATCH`:
  - PATCH for fixes and wording changes that keep how skills are used (0.5.0 → 0.5.1).
  - MINOR for new skills or new behaviour that existing usage still works with (0.5.1 → 0.6.0).
  - MAJOR for breaking changes: a skill removed or renamed, or a workflow that now needs users to work differently (0.6.0 → 1.0.0). While the version is 0.x, breaking changes raise MINOR instead.
- Raise the version once per pull request, relative to the base branch, not once per commit.
- Run `python3 scripts/check_plugin_version.py origin/main` before opening the pull request. The `Plugin version` GitHub check runs the same test and fails the pull request if the versions differ, are not SemVer, or were not raised.
