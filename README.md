# XCALibre Skills

Reusable agent skills for developing, configuring, validating and documenting computational fluid dynamics workflows with [XCALibre.jl](https://github.com/Multiphysics-Flow-Solvers/XCALibre.jl).

The repository is packaged as one marketplace plugin for Claude Code and Codex. Both platforms load the same platform-neutral skill sources.

## Quick start

Install the plugin (see below), then talk to your agent normally. You do not need to name a skill.

| You say | What happens | Skill |
|---|---|---|
| "I'm starting a new feature in XCALibre.jl that adds…" | Creates a feature branch, sets up a small journal in `dev/`, starts a 50-minute progress check, then gets on with the work. | `xcalibre-dev` |
| "Pick up where we left off." | Reads the journal and Git state, restarts the progress check and continues from the recorded next step. | `xcalibre-dev` |
| "The feature is done, wrap it up." | Tidies examples, comments and leftovers, archives the journal and runs the full test gate. | `xcalibre-close` |
| "Open a PR for this feature." | Checks the branch against the project's PR rules, fixes or reports what is missing, and opens the PR from your GitHub account. | `xcalibre-pr` |
| "Review PR 123." | Checks the PR rules, then reviews the code for architecture, CPU/GPU/MPI coverage, performance and correctness. | `xcalibre-review` |

You can still call a skill by name, for example `/xcalibre-skills:xcalibre-pr` in Claude Code or `$xcalibre-pr` in Codex. Commits, pushes, pull requests and posted review comments always need your go-ahead.

## How the skills work

### `xcalibre-dev`: development sessions

Keeps a development session recoverable if it crashes or the machine restarts, and lets you see at a glance where the work is heading.

- **Three small files in `dev/`**, never committed (`dev/` is added to `.git/info/exclude`):
  - `STATUS.md`: goal, branch, what is happening now, the exact next step, questions for you and running agents. Rewritten in place, at most 40 lines. Read this to see where things stand.
  - `journal.md`: one timestamped line per event, such as a direction chosen, an idea refuted or a commit landed.
  - `runs.jsonl`: one line per trial with its numbers, easy to filter with `runs <pattern>` or `jq`.
- **Size limits:** the journal and runs files move to `dev/archive/` when full; raw logs and dumps are not kept. Scripts worth re-running go in `dev/scripts/`.
- **50-minute check:** every 50 minutes the agent updates `STATUS.md`, asks any running agents for progress and tells you if work has stalled.
- **Light touch:** it records the work; it does not tell the agent how to do it.

### `xcalibre-pr`: pull requests

Prepares a PR that meets the XCALibre.jl rules, using a preflight script that reports each check as pass, fail or needs review.

- **One theme per PR.** Unrelated changes are split into separate PRs.
- **Changelog:** never edit `CHANGELOG.md`. Add one file per PR, `changelog/unreleased/<branch-name>.md`, with lines such as `* fixed: Corrects the wall-flux sign in the energy equation.` Each item is at most two sentences and 30 words; the PR description carries the detail.
- **Self-contained:** descriptions, docs and comments justify a change by its mathematics or measured performance, never by what another code does. They cite no case, data or hardware outside XCALibre.jl.
- **Complete:** a fix or feature reaches every solver, backend and code path that shares the behaviour; it comes with tests, docs and an example where needed, and a passing `Pkg.test()`.
- **Authorship:** the PR is opened from the contributor's own account and ends with an AI-assistance line.

### `xcalibre-review`: reviews

An AI review that a human maintainer then confirms.

1. **PR rules:** runs the `xcalibre-pr` preflight; if the PR mixes themes, it proposes a split instead of reviewing.
2. **Code:** checks that the change follows the existing XCALibre.jl API and architecture, works on CPU, GPU and MPI-distributed meshes, and has no obvious performance problems: allocations in solver loops (costly on GPU), type instability, temporary arrays, extra kernel launches or host–GPU transfers. It also points out clear chances to cut allocations or time.
3. **Report:** a short list of verified findings, most severe first, plus any open PR-rule items.

### `xcalibre-close`: wrapping up a feature

Before the PR, it turns the dev journal into a short archive note (what was built, what failed), rewrites examples so they read as examples, trims comments, deletes leftovers and runs the full test gate. It then hands over to `xcalibre-pr`.

### Guidance skills

These load on their own when the work needs them:

| Skill | Use |
|---|---|
| `xcalibre-skills` | Umbrella entry point that routes to the right skill. |
| `julia-benchmarking` | Measuring Julia performance, separating compilation, allocation, data movement and runtime. |
| `xcalibre-kernels` | Writing CPU/GPU kernels and fused field loops in the XCALibre.jl style. |
| `xcalibre-mesh-types` | Keeping mesh code type-stable across float and integer types. |

## Requirements

| Tool | Needed for |
|---|---|
| Python ≥ 3.9 | The workflow skill scripts. |
| Git | The project repository. |
| GitHub CLI (`gh`), signed in | Opening PRs and the authorship checks. |
| Julia | Running `Pkg.test()` before a PR. |

Used the earlier `xcalibre-dev` vault? `resume` lists its files; fold anything still live into `dev/STATUS.md` and move the rest to `dev/archive/`.

## Install in Claude Code

Add the GitHub repository as a marketplace:

```text
/plugin marketplace add mberto79/xcalibre-skills
```

Install the plugin:

```text
/plugin install xcalibre-skills@xcalibre-skills
```

Skills are picked up from what you ask (see **Quick start**). To call one by name, prefix it with the plugin name, for example `/xcalibre-skills:xcalibre-pr`.

Use `/plugin` to inspect installed plugins and marketplace updates.

## Install in Codex

Add the GitHub repository as a marketplace:

```bash
codex plugin marketplace add mberto79/xcalibre-skills --ref main
```

Install the plugin:

```bash
codex plugin add xcalibre-skills@xcalibre-skills
```

Restart Codex if the new skills do not appear immediately. Skills are picked up from what you ask; to call one by name, use `$xcalibre-pr` and so on.

## Update an existing installation

Refresh the marketplace, apply the latest plugin package, then reload it using the instructions for the relevant provider.

**Claude Code**

```text
/plugin marketplace update xcalibre-skills
/plugin update xcalibre-skills@xcalibre-skills
/reload-plugins
```

**Codex**

```bash
codex plugin marketplace upgrade xcalibre-skills
codex plugin add xcalibre-skills@xcalibre-skills
```

Claude Code can perform updates automatically when marketplace auto-update is enabled. Start a new Codex thread after updating so the revised skills are loaded.

## Development installation

Clone the repository only when editing or validating the skill collection locally:

```bash
git clone https://github.com/mberto79/xcalibre-skills.git
cd xcalibre-skills
```

Claude Code can add the local checkout through `/plugin marketplace add /path/to/xcalibre-skills`. Codex can add it from the repository root with:

```bash
codex plugin marketplace add .
codex plugin add xcalibre-skills@xcalibre-skills
```

## Repository structure

```text
xcalibre-skills/
|-- .agents/
|   `-- plugins/
|       `-- marketplace.json
|-- .claude-plugin/
|   `-- marketplace.json
|-- plugins/
|   `-- xcalibre-skills/
|       |-- .claude-plugin/
|       |   `-- plugin.json
|       |-- .codex-plugin/
|       |   `-- plugin.json
|       `-- skills/
|           |-- xcalibre-skills/
|           |-- julia-benchmarking/
|           |-- xcalibre-close/
|           |-- xcalibre-dev/
|           |-- xcalibre-kernels/
|           |-- xcalibre-mesh-types/
|           |-- xcalibre-pr/
|           `-- xcalibre-review/
`-- README.md
```

- `.claude-plugin/marketplace.json` is the Claude Code marketplace catalogue.
- `.agents/plugins/marketplace.json` is the Codex marketplace catalogue.
- `plugins/xcalibre-skills/` is the shared plugin payload.
- Each directory under `plugins/xcalibre-skills/skills/` is an independently selectable skill.

A `src/` directory is not required. These packages are declarative skills rather than a compiled library, and both plugin formats expect their distributable skill content inside the plugin directory.

## Development principles

- Keep shared routing and essential constraints in the umbrella skill.
- Keep each specialist skill focused on one identifiable workflow.
- Keep detailed guidance and deterministic scripts with the specialist skill that uses them.
- Validate technical claims against the relevant XCALibre.jl source and documentation.
- Maintain one canonical skill tree for Claude Code and Codex.
- Commit marketplace-ready changes under the human contributor's identity.

## Platform documentation

- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Claude Code plugin discovery and installation](https://code.claude.com/docs/en/discover-plugins)
- [Codex skills](https://developers.openai.com/codex/skills)
