# Lab 05: Naive box blur

## Prepare

Read NVIDIA's [finite-difference stencil article, Part 1](https://developer.nvidia.com/blog/finite-difference-methods-cuda-cc-part-1/)
for its neighborhood, halo, and data-reuse model. Do not transplant its optimized
kernel: this lab intentionally establishes a naive reference for Chapter 06.

On paper, draw adjacent output pixels and their radius-2 input neighborhoods.
Count the shared input positions, then draw an output pixel at a corner and apply
the lab's clamp rule. You are ready when you can distinguish logical neighborhood
loads from unique input values fetched.

Implement a radius-2 box blur over a single-channel floating-point image. This
is the deliberately redundant baseline that Chapter 06 will tile.

For every output pixel, visit the `5 x 5` neighborhood. Clamp each sampled
coordinate to the nearest valid edge coordinate, sum in `float`, and divide by
25. Launch one thread per output pixel and guard partial blocks.

Run `cuda_box_blur [width] [height]`; test tiny images (`1 x 1`, `2 x 7`) as
well as the awkward default. Use the CPU reference to settle boundary-policy
questions before thinking about speed.

Before moving on, estimate:

- global loads and stores per output pixel;
- how often two neighboring threads fetch the same input value;
- why a larger block does not by itself remove that repeated traffic.
