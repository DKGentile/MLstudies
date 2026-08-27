# Lab 04: 256-bin histogram

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
