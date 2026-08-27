# Nsight profiling worksheet

Complete this before and after each optimization. A profiler report is evidence;
it is not a substitute for a prediction or a wall-clock result.

## 1. Experiment identity

- Date, commit, machine, and exact GPU:
- Executable and kernel:
- Input dimensions/distribution:
- Build command and Release evidence:
- Correctness cases that passed:
- Timing scope and repetition policy:
- Baseline report file:
- Candidate report file:

## 2. Pre-profile hypothesis

- Suspected limiter: `memory traffic / access pattern / atomics / latency /
  arithmetic / launch overhead / synchronization / other`
- Code-level reason:
- Metric expected to change:
- Direction expected:
- Change that would falsify the hypothesis:

For an access claim, write the byte addresses (or element indices) touched by
lanes 0–7 of one representative warp:

```text
lane:       0    1    2    3    4    5    6    7
baseline:
candidate:
```

## 3. Timing validity

Check every box before comparing numbers:

- [ ] Both outputs pass the same CPU reference and boundary policy.
- [ ] Both are built with the same Release flags and target architecture.
- [ ] Input, launch dimensions, warmups, iterations, and batches match.
- [ ] Kernel-only time uses CUDA events on the same stream.
- [ ] The timed region has explicit completion semantics.
- [ ] Allocation and copies are excluded from kernel-only time.
- [ ] H2D, D2H, and end-to-end numbers are labeled separately.
- [ ] Profiler-run duration is not entered as normal benchmark duration.
- [ ] Thermal throttling, display activity, and other GPU work were noted.
- [ ] Several whole-program runs agree closely enough to report a median.

## 4. Capture

Windows PowerShell example (adjust the executable path for the generator):

```powershell
./06_gpu_optimization/profiling/profile.ps1 `
  -Tool ncu `
  -Executable ./build/06_gpu_optimization/02_tiled_blur/Release/gpu_tiled_blur.exe `
  -Kernel 'regex:naive_blur_kernel' `
  -OutputName gtx1080_blur_naive `
  1921 1081
```

Linux/macOS-host-shell example (CUDA execution still requires a supported
NVIDIA environment):

```sh
KERNEL_FILTER='regex:tiled_blur_kernel' \
  ./06_gpu_optimization/profiling/profile.sh ncu \
  ./build/06_gpu_optimization/02_tiled_blur/gpu_tiled_blur \
  rtx5060ti_blur_tiled 1921 1081
```

Use `ncu` for kernel analysis and `nsys` for application/transfer/launch
timelines. The scripts skip cleanly with an explanatory message if the selected
profiler is not installed. Nsight option and metric labels can vary by version;
record the version in `NOTES.md`.

The histogram executable validates a full 256-bin distribution first and then
validates/benchmarks the contended 64-bin distribution. Since Nsight Compute's
`--launch-skip` counts only launches matching the kernel-name filter, skip one
matching launch to profile the same 64-bin workload reported by the timer:

```powershell
./06_gpu_optimization/profiling/profile.ps1 `
  -Tool ncu `
  -Executable ./build/06_gpu_optimization/03_privatized_histogram/Release/gpu_privatized_histogram.exe `
  -Kernel 'regex:shared_histogram_kernel' `
  -LaunchSkip 1 `
  -OutputName gtx1080_hist_shared_64bins
```

```sh
KERNEL_FILTER='regex:shared_histogram_kernel' LAUNCH_SKIP=1 \
  ./06_gpu_optimization/profiling/profile.sh ncu \
  ./build/06_gpu_optimization/03_privatized_histogram/gpu_privatized_histogram \
  rtx5060ti_hist_shared_64bins
```

Use the same skip for `global_atomic_histogram_kernel`. Blur and coalescing use
the first matching launch, so leave the skip at zero. See the
[Nsight Compute CLI filter documentation](https://docs.nvidia.com/nsight-compute/NsightComputeCli/)
when adapting these commands to another capture sequence.

## 5. Evidence table

Enter values exactly as displayed, including units. If a metric is unavailable,
write `N/A (tool/version reason)`.

| Signal | Baseline | Candidate | Interpretation, not just direction |
|---|---:|---:|---|
| Kernel median from harness (ms) | | | |
| Speed of Light: compute throughput (%) | | | |
| Speed of Light: memory throughput (%) | | | |
| DRAM bytes / throughput | | | |
| L1/TEX and L2 hit rates | | | |
| Global load/store sectors or requests | | | |
| Shared-memory throughput / conflicts | | | |
| Atomic-related signal | | | |
| Achieved occupancy (%) | | | |
| Theoretical occupancy (%) | | | |
| Active warps per scheduler | | | |
| Eligible warps per scheduler | | | |
| Dominant warp stall reasons | | | |
| Registers per thread | | | |
| Static + dynamic shared bytes/block | | | |

Occupancy is a capacity/latency-hiding clue, not a score. If the optimized
kernel is faster at lower occupancy, explain what work or traffic it removed.

## 6. Conclusion

- Was the original hypothesis supported, rejected, or unresolved?
- What evidence is strongest?
- What alternative explanation remains?
- What single controlled change comes next?
- What would make the next result non-comparable?

## 7. Cross-GPU interpretation

Repeat with identical functional inputs on the GTX 1080 and RTX 5060 Ti, using
a native build on each. Do not copy an optimized block size blindly: report both
the common configuration and, optionally, a separately tuned configuration.

| Question | GTX 1080 | RTX 5060 Ti |
|---|---|---|
| Same result hash/check? | | |
| Native architecture flag? | | |
| Best measured launch geometry? | | |
| Primary bottleneck evidence? | | |
| Kernel-only improvement? | | |
| End-to-end improvement? | | |
| Why ratios differ? | | |
