# Lab 04: 256-bin histogram

## Prepare

Read the CUDA Programming Guide's [atomics section](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html#atomics).
Separate two claims in your notes:

1. an atomic read-modify-write prevents lost updates at its stated scope; and
2. many threads targeting the same address may still serialize and run slowly.

Before coding, compare 256 uniformly used bins with only 64 active bins for the
same number of input bytes. Predict which case sends more concurrent updates to
the same addresses. Save NVIDIA's optimized histogram article for Chapter 06;
this lab is the deliberately simple baseline.

Count every byte value in the input. Start with the simplest correct global
atomic implementation. Correctness, not cleverness, is the goal in this chapter.

Constraints:

- Use a grid-stride loop so a fixed grid can consume any input size.
- Increment exactly one bin for each byte.
- The harness checks a full-range distribution, then a 64-bin contended
  distribution, zeroing the output between them.
- Do not add host-side counting to the GPU path.

Run `cuda_histogram [byte_count]`; test `1`, `255`, `256`, `257`, and a large
non-power-of-two value. The reported timing uses the 64-bin distribution; record
why it creates contention. Chapter 06 asks you to reduce that contention with a
per-block shared histogram.
