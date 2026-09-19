---
name: xcalibre-mesh-types
description: Use when writing, reviewing, or refactoring XCALibre.jl functions or kernels that accept Mesh2/Mesh3, Cell, Face2D, Face3D, or mesh-derived scalar/index values and need type-stable Float32/Float64 and Int32/Int64 behavior.
---

# XCALibre Mesh Type Parameters

Prefer carrying mesh numeric types as method parameters instead of recovering them inside hot code.

## Core Pattern

Bind the mesh float type from the local object that owns geometry:

```julia
@inline function f(cell::Cell{TF}, face::Face3D{TF}, i::TI) where {TF,TI}
    z = zero(TF)
    one_tf = one(TF)
    ...
end
```

For sparse or field storage, bind the array element type directly:

```julia
@generated function apply!(..., nzval::AbstractArray{TF}, cell::Cell{TF}, cellID::TI) where {TF,TI}
    quote
        acc = zero(TF)
        ...
    end
end
```

## Rules

- Use `cell::Cell{TF}` or `face::Face2D{TF}` / `face::Face3D{TF}` when geometry drives arithmetic type.
- Use `array::AbstractArray{TF}` when sparse matrix or field storage drives arithmetic type.
- Use `cellID::TI`, `fID::TI`, `i::TI`, or separate integer parameters when index type matters.
- Emit `zero(TF)`, `one(TF)`, `TF(0.5)`, and `TF(value)` in generated code and kernels.
- Avoid `0.0`, `1.0`, `0.5`, `eps()`, and `max(x, 0.0)` in hot paths; use `zero(x)`, `one(x)`, `TF(0.5)`, `eps(x)`, and `max(x, zero(x))`.
- Prefer type parameters in the function signature over calling `_get_float(mesh)`, `eltype(...)`, or `oftype(...)` inside per-cell/per-face loops.
- Cast convention: do NOT wrap field/face/cell accesses in `TF()` - they are already typed. DO cast `ConstantScalar` properties, numeric literals, `cell_nsign`, and BC values.
- `SVector{N,TI}`: both `N` and `TI` must be compile-time (type parameters). A runtime `TI` (e.g. from `_get_int(mesh)`) silently kills type stability.

## Boundary Macro Pattern

Boundary condition methods should expose the mesh scalar and index types in the generated signature:

```julia
@inline function (bc::BC)(
    term::Operator{F,P,I,Op}, colval, rowptr, nzval,
    cellID::TI, zcellID::TZI, cell::Cell{TF}, face, fID::TFI, i::TBI,
    component, time,
) where {F,P,I,TF,TI,TZI,TFI,TBI}
    ap, bp = ...
    return TF(ap), TF(bp)
end
```

This stops Float32 meshes accidentally returning Float64 coefficients when a boundary definition uses numeric literals.
