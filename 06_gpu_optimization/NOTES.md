# GPU machine and experiment notes

Create one dated section per machine/toolchain combination. Preserve previous
sections after upgrades: performance without environment metadata is anecdote,
not a reproducible result.

## Machine: `<GTX 1080 | RTX 5060 Ti | other>`

- Date/time and timezone:
- Git commit and local-change note:
- Host name / role:
- OS and kernel/build:
- CPU and RAM:
- GPU exact name (`nvidia-smi -L`):
- VRAM:
- Compute capability (verified with `deviceQuery` or trusted documentation):
- GPU used for display? `yes/no`:
- Driver (`nvidia-smi`):
- CUDA compiler (`nvcc --version`):
- CUDA runtime printed by harness:
- Host compiler:
- CMake version and generator:
- Build type / configuration:
- `CMAKE_CUDA_ARCHITECTURES`:
- Nsight Compute version:
- Nsight Systems version:
- Power limit / persistence mode if known:
- Temperature before and after run:
- Other active GPU processes:

### Exact commands

```text
# Configure

# Build

# Correctness runs, including odd/tiny cases

# Benchmark

# Profile
```

### Measurement controls

- Input shape and deterministic seed/pattern:
- Warmups, iterations per batch, batches:
- Timing scope (`CPU`, `kernel-only`, `H2D`, `D2H`, `end-to-end`):
- Number of whole-program reruns:
- Clock/power/thermal variance observed:
- Profiler replay overhead excluded from benchmark table? `yes/no`:

### Change log

| Change | Correct? | Hypothesis | Result | Keep/revert and why |
|---|---|---|---|---|
| Baseline | | | | |
| | | | | |

### Non-comparability warnings

- Different toolkits, flags, dimensions, timing scopes, or machine load:
- Missing machine and concrete reason:

