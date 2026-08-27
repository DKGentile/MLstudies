# Lab 05: Naive box blur

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

