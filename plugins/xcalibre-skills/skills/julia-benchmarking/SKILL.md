---
name: julia-benchmarking
description: Use when benchmarking Julia performance, especially when isolating a representative subproblem from a larger application and separating compilation, allocation, data movement, and steady-state runtime.
---

# Julia Benchmarking

- Benchmark extracted kernels or data slices that preserve the real bottleneck, not only full applications.
- Always separate first-run compilation from warmed steady-state timings.
- Run at least one warmup with the same types, backend, sizes, and control path as the measured case.
- For full simulation benchmarks, `@time run!(...)` wall time is acceptable after a one-iteration `run!` warmup that compiles the solver path; then rebuild the configuration object with the target iteration count and reinitialise all fields with `initialise!` before measuring.
- Time setup/update/apply phases separately; total time alone hides the cause.
- Track allocations and data movement, especially CPU/GPU transfers and sparse-matrix conversions.
- Prefer representative serialized inputs so runs are deterministic and fast to repeat.
- Compare against the baseline in the same process or with equivalent warmup.
- Change one variable at a time and keep the benchmark command in the final report.
- Treat surprising speedups or slowdowns as suspect until repeated after warmup.
- After performance changes, validate correctness with the focused test and, when feasible, the full workflow.
