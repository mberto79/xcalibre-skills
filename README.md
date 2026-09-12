# XCALibre Skills

Reusable agent skills for developing, configuring, validating and documenting computational fluid dynamics workflows with XCALibre.jl.

## Status

This repository contains an umbrella XCALibre skill and six specialist skills for XCALibre.jl and Julia development workflows.

The root `SKILL.md` can be installed as a standalone umbrella skill in Claude Code or Codex. Claude marketplace and Codex plugin packaging will be added before the first packaged release.

## Repository structure

```text
xcalibre-skills/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- assets/
|-- references/
|-- scripts/
`-- skills/
    |-- julia-benchmarking/
    |-- xcalibre-close/
    |-- xcalibre-dev/
    |-- xcalibre-kernels/
    |-- xcalibre-mesh-types/
    `-- xcalibre-pr/
```

- `SKILL.md`: shared, platform-neutral skill instructions.
- `agents/openai.yaml`: optional OpenAI and Codex interface metadata.
- `assets/`: templates and other files used in generated outputs.
- `references/`: technical material loaded only when relevant.
- `scripts/`: reusable automation where deterministic execution is useful.
- `skills/`: specialist skills and their supporting resources.

## Available skills

| Skill | Description and use |
|---|---|
| `xcalibre-skills` | Umbrella entry point for the complete collection. Use `/xcalibre-skills` in Claude Code or `$xcalibre-skills` in Codex for general XCALibre.jl work or when the appropriate specialist skill is not known. It selects and loads only the relevant specialist guidance. |
| `julia-benchmarking` | Provides reliable Julia performance measurement by separating compilation, allocation, data movement and warmed steady-state runtime. Use it when designing or reviewing benchmarks, isolating a representative bottleneck, or comparing CPU and GPU implementations. |
| `xcalibre-kernels` | Provides XCALibre.jl conventions for fused field loops and `KernelAbstractions.jl` kernels across CPU and GPU backends. Use it when adding, reviewing or refactoring computational kernels and backend-independent field operations. |
| `xcalibre-mesh-types` | Preserves type stability for `Mesh2`, `Mesh3`, cells, faces and mesh-derived scalar or index values. Use it when code must work correctly with `Float32`, `Float64`, `Int32` and `Int64` mesh configurations. |
| `xcalibre-dev` | Maintains a persistent context vault for substantial features, phases, refactors and debugging campaigns. Use it when engineering work must remain recoverable and understandable across multiple development sessions. Do not use it for small edits, reviews or general questions. |
| `xcalibre-close` | Consolidates and cleans the records, examples, documentation and generated evidence at feature or development close. It runs the `xcalibre-pr` preflight checks and reports readiness, but does not commit, push, merge or open a pull request. Invoke `xcalibre-pr` separately for submission. |
| `xcalibre-pr` | Checks and prepares an XCALibre.jl contribution for submission. Use it to verify branch synchronisation, PR scope, changelog entries, tests, documentation, examples, comment length, dependencies, licences, human authorship and AI disclosure. It lists unresolved items and requires consent before corrective work or submission actions. |

With the standalone installation, invoke the umbrella skill and name the required workflow. Platform-specific packaging will also expose the specialist skills directly as `/skill-name` in Claude Code and `$skill-name` in Codex.

## Install in Claude Code

Claude Code loads personal skills from `~/.claude/skills/` and project skills from `.claude/skills/`.

### Personal installation

Repository URL: `https://github.com/mberto79/xcalibre-skills.git`

macOS and Linux:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/mberto79/xcalibre-skills.git ~/.claude/skills/xcalibre-skills
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/mberto79/xcalibre-skills.git "$HOME\.claude\skills\xcalibre-skills"
```

Restart Claude Code if the skill does not appear immediately. Confirm installation with `/skills`, then invoke the skill with `/xcalibre-skills`.

### Project installation

To make the skill available only within an XCALibre.jl checkout, clone it into the project-level skill directory:

```bash
cd /path/to/XCALibre.jl
mkdir -p .claude/skills
git clone https://github.com/mberto79/xcalibre-skills.git .claude/skills/xcalibre-skills
```

For a team-managed XCALibre.jl repository, use a Git submodule instead of committing a nested clone:

```bash
git submodule add https://github.com/mberto79/xcalibre-skills.git .claude/skills/xcalibre-skills
```

See the official [Claude Code skills documentation](https://code.claude.com/docs/en/skills) for skill scopes and discovery behaviour.

## Install in Codex

Codex loads personal skills from `~/.agents/skills/` and repository skills from `.agents/skills/`.

### Personal installation

macOS and Linux:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/mberto79/xcalibre-skills.git ~/.agents/skills/xcalibre-skills
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
git clone https://github.com/mberto79/xcalibre-skills.git "$HOME\.agents\skills\xcalibre-skills"
```

Restart Codex if the skill does not appear immediately. Invoke it explicitly with `$xcalibre-skills`, or allow Codex to select it automatically for matching XCALibre.jl tasks.

### Project installation

To make the skill available only within an XCALibre.jl checkout:

```bash
cd /path/to/XCALibre.jl
mkdir -p .agents/skills
git clone https://github.com/mberto79/xcalibre-skills.git .agents/skills/xcalibre-skills
```

For a team-managed repository:

```bash
git submodule add https://github.com/mberto79/xcalibre-skills.git .agents/skills/xcalibre-skills
```

See the [official OpenAI skill documentation](https://developers.openai.com/codex/skills) for Codex skill locations and discovery behaviour.

## Use with XCALibre.jl

1. Install the skill at personal or project scope.
2. Open the XCALibre.jl checkout as the working project.
3. Invoke the skill explicitly when required.

Claude Code:

```text
/xcalibre-skills inspect this XCALibre.jl case and explain the solver configuration.
```

Codex:

```text
$xcalibre-skills inspect this XCALibre.jl case and explain the solver configuration.
```

## Update an installation

Run `git pull` inside the installed `xcalibre-skills` directory. Restart the host application if it does not detect the changes automatically.

## Development principles

- Keep shared routing and essential constraints in `SKILL.md`.
- Keep detailed technical guidance in focused files under `references/`.
- Add scripts only when repeatable automation improves correctness or reliability.
- Keep each specialist skill focused on one identifiable XCALibre.jl or Julia development workflow.
- Validate technical claims against the relevant XCALibre.jl source and documentation.
- Keep one neutral source tree under `skills/`; generate or package platform-specific layouts from that source rather than maintaining divergent Claude and Codex copies.

## Claude marketplace release

The marketplace release will add:

```text
.claude-plugin/marketplace.json
plugins/xcalibre-skills/.claude-plugin/plugin.json
plugins/xcalibre-skills/skills/
```

The final marketplace installation command will be documented after the marketplace manifests are added and validated.
