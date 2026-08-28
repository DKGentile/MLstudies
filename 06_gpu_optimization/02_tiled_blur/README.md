# Stage 02: Tile a box blur

## Prepare

Read NVIDIA's [shared-memory article](https://developer.nvidia.com/blog/using-shared-memory-cuda-cc/)
and the neighborhood/halo discussion in its
[finite-difference stencil article](https://developer.nvidia.com/blog/finite-difference-methods-cuda-cc-part-1/).

Before coding, draw one output block, its radius-2 halo, and the larger shared
tile. Calculate the number of output elements, tile elements, and naive input
requests. Then state the barrier invariant: no thread may consume the shared tile
until all cooperative loads needed by any active output have completed.

The file contains a complete CPU reference and naive global-memory GPU baseline.
Implement `tiled_blur_kernel` without changing those references.

## Contract

- Radius is 2; every output averages a clamped `5 x 5` neighborhood.
- The launch uses `32 x 8` threads. Do not assume image dimensions are multiples
  of either value.
- Cooperatively load the block footprint plus its halo into dynamic shared
  memory. The shared tile is `(blockDim.x + 4) x (blockDim.y + 4)`.
- A thread may load more than one tile element.
- All shared values needed by any active output thread must be initialized.
- Every block thread must reach the load/compute barrier, including threads whose
  output coordinates lie outside the image.
- Once the tile is populated, stencil reads must come from shared memory.

Run `gpu_tiled_blur [width] [height]`. Start with `1 x 1`, `31 x 7`, `32 x 8`,
and `33 x 9`; only then use the default `1921 x 1081`.

## Design questions

1. How many tile elements and output elements does a full block own?
2. Map a linear cooperative-load index to tile `(x, y)` and then global `(x, y)`.
3. Which global coordinates need clamping at image boundaries?
4. Which barrier is necessary, and what data dependency does it protect?
5. Count naive loads and approximate tiled loads per full output block. This is
   traffic requested by your code, not necessarily DRAM traffic after caching.

After correctness passes, capture naive and tiled profiles using the same shape.
Do not call the kernel faster merely because theoretical occupancy is higher;
correlate time with memory-workload and scheduler evidence.
