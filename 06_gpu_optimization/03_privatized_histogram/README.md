# Stage 03: Privatize a contended histogram

The baseline sends every increment to one of 256 bins in global memory. The
harness first validates all 256 byte values, then validates and benchmarks a
64-bin distribution that creates heavier contention. Implement a per-block
shared-memory histogram and merge 256 block-local counts into the global result.

## Contract

- Initialize all shared bins cooperatively, then synchronize.
- Consume arbitrary input lengths with a grid-stride loop.
- Use atomics for contended shared updates.
- Synchronize before any thread merges shared bins to global memory.
- Merge every bin exactly once per block (or in a correct cooperative pattern).
- The harness initializes global output arrays; the kernel owns shared state.

Run `gpu_privatized_histogram [byte_count]`. Test `1`, `255`, `256`, `257`, and
the default. Then modify only the input distribution (for example 64 active bins
versus 256) and predict whether privatization should help more or less.

## Evidence questions

- How many global atomic operations does each design request?
- Does the profiler show a different atomic or serialization bottleneck?
- Does shared-memory initialization/merge dominate at small input sizes?
- Does reported occupancy change because of shared-memory use, and does that
  change correlate with time?
- Do the GTX 1080 and RTX 5060 Ti rank the two kernels by the same ratio?
