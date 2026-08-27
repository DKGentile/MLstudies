# Lab 03: Block reduction

Produce one partial sum per block. The host intentionally performs the final
sum, keeping this exercise focused on safe cooperation inside one block.

Requirements:

- Each block consumes up to `2 * blockDim.x` input values.
- Stage per-thread sums in the provided dynamic shared-memory array.
- Every thread in the block must reach each required barrier.
- Handle a tail that is smaller than a full block without reading past `n`.
- Write exactly one value per block to `partial_sums`.

Run `cuda_reduction [element_count]`. Useful adversarial sizes are `1`, `255`,
`256`, `511`, `512`, `513`, and `1048589`.

After it passes, explain why moving `__syncthreads()` under `if (global < n)` can
deadlock, and why shared memory cannot directly synchronize two blocks.

