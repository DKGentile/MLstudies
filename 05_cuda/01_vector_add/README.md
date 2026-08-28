# Lab 01: Vector addition

## Prepare

Required before coding:

- Read the CUDA Programming Guide's [thread-block and grid model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html#thread-blocks-and-grids).
  Draw one 1-D grid and label `threadIdx.x`, `blockIdx.x`, `blockDim.x`, and
  `gridDim.x`.
- Read NVIDIA's [grid-stride-loop explanation](https://developer.nvidia.com/blog/cuda-pro-tip-write-flexible-kernels-grid-stride-loops/).
  Focus on the index increment and why it permits fewer threads than elements.

Before opening `main.cu`, derive the first two indices owned by thread 0 and the
last launched thread. You are ready when you can explain why both a loop and an
`i < n` guard are required by this harness.

Implement `out[i] = a[i] + b[i]` in `vector_add_kernel`.

Constraints:

- Use a grid-stride loop, so correctness does not depend on launching one thread
  per element.
- Never read or write outside `[0, n)`.
- Do not change the CPU reference or tolerance to make a bad kernel pass.

Run `cuda_vector_add [element_count]`. Try `1`, `255`, `256`, `257`, and
`1048583`. Before coding, answer: what values can the first thread in the final
block use as its global index and stride? The harness caps the launch at 256
blocks, so the default case cannot pass with a single guarded add per thread.
