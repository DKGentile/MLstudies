# Chapter 06: GPU optimization by evidence

The goal is not merely a faster kernel. The goal is a defensible optimization
story: a correct baseline, a stated bottleneck hypothesis, one controlled
change, a repeatable measurement, and profiler evidence that supports or rejects
the hypothesis.

## Stages

| Stage | Work product | Question you must answer |
|---|---|---|
| 01 Coalescing experiment | Bandwidth table for two thread/address mappings | What addresses does one warp request? |
| 02 Tiled blur | Correct shared-memory kernel and speedup | Did reuse reduce global-memory work enough to matter? |
| 03 Privatized histogram | Correct per-block histogram and speedup | Did fewer global atomics move the bottleneck? |
| 04 Profiling | Completed worksheet and saved reports | Which metric falsifies your first hypothesis? |
| 05 Cross-GPU report | GTX 1080 and RTX 5060 Ti result rows | Which architectural difference plausibly explains the gap? |

The optimized blur and histogram kernels contain `TODO(learner)` regions. The
repository supplies correctness references and naive baselines, not completed
optimized kernels.

## Build

```sh
cmake -S 06_gpu_optimization -B build/06_gpu_optimization -DCMAKE_BUILD_TYPE=Release
cmake --build build/06_gpu_optimization --config Release --parallel
```

Targets are `gpu_coalescing`, `gpu_tiled_blur`, and
`gpu_privatized_histogram`. CMake defaults to the architecture of the installed
GPU. Reconfigure and rebuild on each machine; record the resulting architecture
in [NOTES.md](NOTES.md).

Use CUDA 12.x and architecture `61` for the Pascal GTX 1080. The RTX 5060 Ti is
Blackwell architecture `120` and needs CUDA 12.8 or newer. CUDA 12.8/12.9 can
compile both; CUDA 13 removed Pascal offline compilation, so a CUDA 13 install
cannot build the GTX target. Verify locally with `nvcc --list-gpu-code`; see the
[NVIDIA architecture matrix](https://docs.nvidia.com/datacenter/tesla/drivers/latest/cuda-toolkit-driver-and-architecture-matrix.html)
and [CUDA 13 release notes](https://docs.nvidia.com/cuda/archive/13.0.1/cuda-toolkit-release-notes/index.html).

If CUDA is unavailable, configuration succeeds and emits a clear skip target:

```sh
cmake -S 06_gpu_optimization -B build/06-no-cuda -DMLSTUDIES_ENABLE_CUDA=OFF
cmake --build build/06-no-cuda
python 06_gpu_optimization/tests/validate_course.py
```

The validator and the forced-skip build require no GPU, driver, CUDA toolkit, or
Python packages beyond the standard library. If `cmake` itself is unavailable,
only the Python validator can run; it validates structure and methodology, not
CUDA compilation. On a toolkit-only host with no visible GPU, explicitly pass
`MLSTUDIES_ENABLE_CUDA=OFF` to avoid native architecture detection.

## Optimization loop

For every change, keep this order:

1. Define the exact output and edge behavior.
2. Pass the CPU-reference check on adversarial dimensions.
3. Write a bottleneck hypothesis before opening a profiler.
4. Measure a Release build with fixed data, warmups, and repeated samples.
5. Profile one representative launch, not a long benchmark loop.
6. Change one mechanism: access order, reuse, synchronization, atomics, or
   launch geometry.
7. Re-run correctness, timing, and the same profiler sections.
8. Record a rejected hypothesis as carefully as a successful optimization.

The harness reports the median of CUDA-event batches for kernel-only time.
Where shown, end-to-end time includes synchronous H2D copy, kernel, and D2H
copy. CPU time uses a wall clock. These numbers answer different questions and
must remain separate.

## GTX 1080 versus RTX 5060 Ti

Build and profile natively on both systems. Use identical input data and shapes,
but do not expect identical optimal launch parameters. Record driver, toolkit,
clock/power state, display use, and temperature. Compare:

- correctness first;
- kernel median and variability;
- effective bandwidth or throughput using the same byte/work definition;
- achieved and theoretical occupancy, without treating occupancy as speed;
- memory throughput, cache behavior, warp stalls, and atomic behavior;
- transfer and end-to-end time separately from kernel time.

A ratio alone is not an explanation. “The RTX is newer” is not a profiler-backed
claim. Conversely, a lower occupancy value does not prove a kernel is worse if
it has enough active warps to hide latency and does less total work.

Start with [profiling/WORKSHEET.md](profiling/WORKSHEET.md), run the helper script
for your shell, and copy final measurements into
[results/BENCHMARK_TEMPLATE.md](results/BENCHMARK_TEMPLATE.md).

## Definition of done

- Both TODO kernels pass for tiny, odd, and normal input sizes.
- Every table identifies build type and timing scope.
- At least one Nsight Compute report exists for naive and optimized variants.
- You can draw the global-memory transactions for one warp in each kernel.
- You can explain shared-memory lifetime and every barrier in your code.
- You can state why occupancy helped, did not help, or was not limiting.
- GTX 1080 and RTX 5060 Ti rows are present, or the missing run has a dated,
  concrete reason in the report.
