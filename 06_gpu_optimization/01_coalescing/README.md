# Stage 01: Coalescing experiment

## Prepare

Read the CUDA Best Practices Guide sections on
[bandwidth](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#bandwidth) and
[coalesced global-memory access](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/#coalesced-access-to-global-memory).

Before running the code, write the byte address—not merely the `(x, y)`
coordinate—requested by lanes 0 through 7 in each mapping. Also write the useful
bytes divided by elapsed time formula you will call effective bandwidth. The
profile should test that prediction, not substitute for making it.

Both supplied kernels perform the same copy-scale operation and produce the same
row-major output. The row launch uses `256 x 1` blocks; the column launch uses
`1 x 256` blocks. This makes adjacent lanes vary `x` in one kernel and `y` in
the other without adding division/modulo work to only one variant.

1. Predict the first eight addresses requested by a warp in each kernel.
2. Run `gpu_coalescing [width] [height]` in Release mode.
3. Use the default `4096 x 2048` first: both axes are multiples of 256, so both
   launches create the same number of active and total threads. Treat odd sizes
   as correctness tests, not controlled timing comparisons.
4. Repeat at `2048 x 4096`. Then vary width through `31`, `32`, and `33` only as
   a secondary experiment, explicitly recording different padding overhead.
5. Profile one launch of each kernel. Record memory throughput and the profiler's
   sector/request or coalescing-related metric (labels vary by Nsight version).
6. Explain why both kernels can have similar arithmetic and occupancy but very
   different memory behavior.

This is a controlled diagnostic, so both kernels are supplied. Your work is the
prediction, experiment design, profiler capture, and explanation—not rewriting
the benchmark until it confirms your expectation.
