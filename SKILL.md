---
name: xcalibre-skills
description: Support XCALibre.jl computational fluid dynamics and aerodynamics workflows. Use for XCALibre.jl setup, modelling, simulation, validation, post-processing, or technical guidance.
---

# XCALibre Skills

Provide the shared entry point for XCALibre.jl workflows.

## Scope

- Preserve the user's stated technical objective and constraints.
- Base technical claims on the available XCALibre.jl source, documentation, or supplied evidence.
- Use British English in explanations and generated material.

## Sub-skill routing

When a task matches a specialised skill under `skills/`, read that skill's `SKILL.md` and apply its instructions. Use only the sub-skills relevant to the task.

- `skills/julia-benchmarking/`: isolate and measure Julia performance accurately.
- `skills/xcalibre-kernels/`: write and review idiomatic XCALibre.jl CPU and GPU kernels.
- `skills/xcalibre-mesh-types/`: preserve numeric and index type stability in mesh code.
- `skills/xcalibre-pr/`: check, prepare, and submit XCALibre.jl pull requests.
- `skills/xcalibre-dev/`: maintain a persistent context vault for substantial development work.
- `skills/xcalibre-close/`: close and archive work managed through `xcalibre-dev`.

Treat `xcalibre-dev` and `xcalibre-close` as development workflow skills. Apply their repository-changing and Git operations only when the user has authorised the corresponding changes.

## Resources

- Read supporting material from `references/` only when relevant.
- Use reusable automation from `scripts/` when it improves reliability.
- Use files from `assets/` only as inputs to generated outputs.
