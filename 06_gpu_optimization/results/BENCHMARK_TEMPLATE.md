# GPU optimization benchmark report

Duplicate the result sections for each meaningful code or toolchain revision.
Keep raw profiler reports outside Git if large; record their exact filenames and
checksums or durable storage location.

## Experiment

- Date and commit:
- Problem/kernel:
- Input shape/distribution:
- Correctness cases passed:
- Output checksum or concise identity check:
- Baseline definition:
- Optimized definition:
- One controlled change:
- Pre-measurement hypothesis:
- Warmups / iterations per batch / batches / whole-program reruns:

## Environment

| Field | GTX 1080 | RTX 5060 Ti |
|---|---|---|
| Run completed? If no, dated reason | | |
| OS / CPU | | |
| Exact GPU / VRAM | | |
| Driver | | |
| CUDA toolkit/runtime | | |
| Compute capability | | |
| CUDA architecture flag | | |
| Build type and flags | | |
| Nsight Compute / Systems | | |
| Power / temperature / display notes | | |

## Correctness

| Machine | Tiny case | Odd-size case | Main case | CPU/GPU tolerance or exact rule |
|---|---|---|---|---|
| GTX 1080 | | | | |
| RTX 5060 Ti | | | | |

## Timing results

Use milliseconds and a median unless the column states otherwise. Put `N/M`
for “not measured,” never zero. Kernel timings exclude allocation and copies.

| Machine | CPU ms | H2D ms | Naive kernel ms | Optimized kernel ms | D2H ms | Optimized end-to-end ms | Kernel speedup | Run-to-run spread |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GTX 1080 | | | | | | | | |
| RTX 5060 Ti | | | | | | | | |

Definitions used for derived throughput:

```text
useful bytes =
operations =
effective GB/s = useful bytes / kernel seconds / 1e9
effective work/s = operations / kernel seconds
```

Do not silently change a byte or operation definition between rows.

## Profiler evidence

| Machine / variant | Memory throughput | Compute throughput | DRAM bytes | Cache evidence | Atomic/shared evidence | Achieved occupancy | Registers/thread | Shared bytes/block | Dominant stalls |
|---|---:|---:|---:|---|---|---:|---:|---:|---|
| GTX 1080 naive | | | | | | | | | |
| GTX 1080 optimized | | | | | | | | | |
| RTX 5060 Ti naive | | | | | | | | | |
| RTX 5060 Ti optimized | | | | | | | | | |

- GTX 1080 naive report:
- GTX 1080 optimized report:
- RTX 5060 Ti naive report:
- RTX 5060 Ti optimized report:

## Analysis

- First bottleneck (memory / compute / atomic / launch / synchronization / other):
- Evidence for that diagnosis:
- What changed in the code:
- Expected metric movement:
- Actual metric movement:
- Hypothesis supported, rejected, or unresolved:
- Why occupancy did or did not matter:
- Why the speedup differs between GTX 1080 and RTX 5060 Ti:
- Kernel-only versus end-to-end implication:
- Remaining correctness or measurement risk:
- Next single experiment:

