---
name: xcalibre-skills
description: Support XCALibre.jl computational fluid dynamics and aerodynamics workflows. Use for XCALibre.jl setup, modelling, simulation, validation, post-processing, or technical guidance.
---

# XCALibre Skills

Shared entry point for XCALibre.jl workflows.

## Scope

- Preserve the user's stated technical objective and constraints.
- Base technical claims on the available XCALibre.jl source, documentation, or supplied evidence.
- Use British English in explanations and generated material.

## Sub-skill routing

When a task matches a specialised sibling skill, read its `SKILL.md` and apply its instructions; use only the sub-skills relevant to the task.

- `../julia-benchmarking/`: isolate and measure Julia performance accurately.
- `../xcalibre-kernels/`: write and review idiomatic XCALibre.jl CPU and GPU kernels.
- `../xcalibre-mesh-types/`: preserve numeric and index type stability in mesh code.

`../xcalibre-dev/`, `../xcalibre-close/`, `../xcalibre-pr/` and `../xcalibre-review/` are direct-invocation workflow skills. Never auto-select them from this umbrella; use one only when the user explicitly invokes it by name or unambiguously asks for that exact workflow (opening/resuming a development vault, closing a phase or feature, preparing/submitting a pull request, or reviewing one), and apply its repository-changing, Git and posting operations only when the user has authorised those changes.

## Resources

Use the selected specialist skill's references and scripts only when that skill requires them.
