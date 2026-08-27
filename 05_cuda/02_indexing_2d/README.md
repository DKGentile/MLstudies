# Lab 02: Two-dimensional indexing

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

