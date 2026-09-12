# XCALibre Skills

Reusable agent skills for developing, configuring, validating and documenting computational fluid dynamics workflows with XCALibre.jl.

## Status

This repository is at the initial development stage. The root `SKILL.md` can be installed as a standalone skill in Claude Code or Codex.

Claude marketplace packaging will be added before the first marketplace release. That release will include the required plugin and marketplace manifests.

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
```

- `SKILL.md`: shared, platform-neutral skill instructions.
- `agents/openai.yaml`: optional OpenAI and Codex interface metadata.
- `assets/`: templates and other files used in generated outputs.
- `references/`: technical material loaded only when relevant.
- `scripts/`: reusable automation where deterministic execution is useful.
- `skills/`: reserved for future specialist XCALibre skills.

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
- Keep each future specialist skill focused on one identifiable XCALibre.jl workflow.
- Validate technical claims against the relevant XCALibre.jl source and documentation.

## Claude marketplace release

The marketplace release will add:

```text
.claude-plugin/marketplace.json
plugins/xcalibre-skills/.claude-plugin/plugin.json
plugins/xcalibre-skills/skills/
```

The final marketplace installation command will be documented after the marketplace manifests are added and validated.
