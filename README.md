# XCALibre Skills

Reusable agent skills for developing, configuring, validating and documenting computational fluid dynamics workflows with [XCALibre.jl](https://github.com/Multiphysics-Flow-Solvers/XCALibre.jl).

The repository is packaged as one marketplace plugin for Claude Code and Codex. Both platforms load the same platform-neutral skill sources.

## Available skills

| Skill | Description and use |
|---|---|
| `xcalibre-skills` | Umbrella entry point for the collection. Use it for general XCALibre.jl work or when the appropriate specialist skill is not known. It selects and loads only the relevant specialist guidance, and never auto-invokes the direct-invocation skills below. |
| `julia-benchmarking` | Separates compilation, allocation, data movement and warmed steady-state runtime. Use it to design or review Julia benchmarks and compare CPU or GPU implementations. |
| `xcalibre-kernels` | Applies XCALibre.jl conventions for fused field loops and `KernelAbstractions.jl` kernels. Use it when adding, reviewing or refactoring backend-independent field operations. |
| `xcalibre-mesh-types` | Preserves type stability for meshes, cells, faces and mesh-derived values. Use it when code must support different floating-point and integer mesh types. |
| `xcalibre-dev` *(direct invocation only)* | Maintains a persistent context vault for substantial features, phases, refactors and debugging campaigns, recoverable across sessions. The vault (`dev/`) is its own Git repository with an optional private GitHub remote, excluded from the project so it never enters a pull request. Several features can be developed at once, each on its own project branch: `dev/features/INDEX.md` binds every feature vault to its branch, and `resume` and `plan` follow whichever branch is checked out. Operations: `doctor`, `init [--feature <slug> [--branch <name>]] [--remote]`, `sync`, `plan <milestone-id> <slug>`, `resume [--full]`, `check`, `migrate [--apply]`. |
| `xcalibre-close` *(direct invocation only)* | Consolidates and cleans development records, examples, documentation and generated evidence at phase or feature close. Runs the `xcalibre-pr` preflight checks but does not submit a pull request. |
| `xcalibre-pr` *(direct invocation only)* | Checks and prepares an XCALibre.jl contribution for submission: branch synchronisation, scope, changelog entries, tests, documentation, examples, comments, dependencies, licences, authorship and AI disclosure. Operations: `preflight [--pr-number <n>] [--confirm <review>]`, `next-number`. Corrective and submission actions require user consent. |
| `xcalibre-review` *(direct invocation only)* | AI review of an XCALibre.jl pull request or diff. Gates on single-theme scope (via `xcalibre-pr`'s preflight) before reviewing correctness, style, and GPU/`KernelAbstractions.jl` compatibility. Call syntax: `xcalibre-review [target] [level] [--comment] [--fix]`, matching `code-review`. Marks output as AI-generated; a human performs the final review and merge. |

Skills marked *(direct invocation only)* are never selected automatically by `xcalibre-skills` or the agent — invoke them explicitly by name.

## First run and requirements

The guidance skills (`xcalibre-skills`, `julia-benchmarking`, `xcalibre-kernels`, `xcalibre-mesh-types`) need nothing beyond the agent. The workflow skills (`xcalibre-dev`, `xcalibre-close`, `xcalibre-pr`, `xcalibre-review`) run local tools. The first time you invoke `xcalibre-dev`, the agent:

1. Runs `xcalibre-dev doctor` to check the tools below.
2. If anything is missing, asks you **once** to approve installing it and creating a private vault repository on your GitHub account. Nothing is installed or created without that approval.
3. Installs what you approved with your platform's package manager (`apt` on Linux, `brew` on macOS, `winget` on Windows), and runs `gh auth login` if you are not signed in to GitHub.
4. Runs `xcalibre-dev init --remote`. This creates the vault in `dev/` as its own Git repository and excludes `dev/` from your project through `.git/info/exclude`, so vault files never appear in your commits or pull requests. It then creates a **private** GitHub repository, `<your-account>/<project>-dev-vault`, and pushes the vault to it. If that repository already exists (for example, when you work on another machine), `init --remote` clones it instead.

| Tool | Needed for |
|---|---|
| Python ≥ 3.9 | Every workflow skill script. Install it yourself if it is missing, because `doctor` itself runs on Python. |
| Git | The project repository and the vault repository. |
| GitHub CLI (`gh`), signed in | Creating and cloning the private vault repository, and the `xcalibre-pr` authorship checks. |
| Julia | Running `Pkg.test()` in `xcalibre-pr` preflight. |

Already using `xcalibre-dev`? Your existing `dev/` is adopted without changing any record. `resume` checks that `dev/` is excluded from the project. If your project still tracks vault files, `resume` tells you to run `git rm -r --cached dev` and commit, which stops tracking them without deleting them.

## Install in Claude Code

Add the GitHub repository as a marketplace:

```text
/plugin marketplace add mberto79/xcalibre-skills
```

Install the plugin:

```text
/plugin install xcalibre-skills@xcalibre-skills
```

Claude Code namespaces plugin skills with the plugin name. Examples:

```text
/xcalibre-skills:xcalibre-pr check this branch for PR readiness
/xcalibre-skills:xcalibre-kernels review this kernel
```

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

Restart Codex if the new skills do not appear immediately. Invoke a skill explicitly or allow Codex to select it for a matching task:

```text
$xcalibre-pr check this branch for PR readiness
$xcalibre-kernels review this kernel
```

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
