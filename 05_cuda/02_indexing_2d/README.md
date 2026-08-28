# Lab 02: Two-dimensional indexing

## Prepare

Read the CUDA Programming Guide's [thread hierarchy and built-in variables](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html#thread-hierarchy).
Pay attention to which coordinate varies fastest when threads are linearized.

Before coding, derive these symbolically rather than memorizing a snippet:

- global `x` from `blockIdx.x`, `blockDim.x`, and `threadIdx.x`;
- global `y` from the corresponding `.y` values; and
- the row-major offset for `(x, y)` in an image of width `W`.

Then test the derivation on paper for a partial block. The checkpoint is whether
you can identify which threads exist but own no valid pixel.

Map a 2-D launch to a row-major image. For pixel `(x, y)`, compute:

```text
output[y, x] = 1.25 * input[y, x] + 0.01 * y + 0.001 * x
```

The default `641 x 479` dimensions deliberately leave partial blocks on both
axes. Run `cuda_indexing_2d [width] [height]`; also test skinny images such as
`1 x 513` and `777 x 1`.

On paper, write the global `(x, y)` coordinate and linear address used by
threads `(0, 0)` and `(15, 15)` in block `(2, 3)`. Then implement only the
marked kernel region.
