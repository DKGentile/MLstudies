# Chapter 05: CUDA fundamentals

This chapter turns the CUDA programming model into muscle memory. Each lab is a
small executable with a CPU reference, deliberately incomplete GPU kernel, and a
correctness gate. Implement only the `TODO(learner)` regions; the harness tells
you when your kernel is correct and then reports a kernel-only timing.

## Learning path

| Lab | Problem | Primary idea | Done when |
|---|---|---|---|
| 01 | Vector addition | 1-D global indexing and bounds checks | Odd-sized inputs pass |
| 02 | 2-D affine transform | Grid/block coordinates and row-major layout | Non-multiple image sizes pass |
| 03 | Sum reduction | Cooperation, barriers, and shared memory | Every tested tail size passes |
| 04 | Byte histogram | Atomics and contention | All 256 bins match the CPU |
| 05 | Box blur | 2-D neighborhoods and boundary policy | CPU and GPU images agree |

## Resource route

Use the resource beside the lab, then return to the kernel. The NVIDIA guide is
the language/runtime contract; the blog posts are focused explanations by CUDA
engineers. Read optimized variants only after your own baseline is correct.

| Lab | Core preparation | What you must extract |
|---|---|---|
| 01 | CUDA Programming Guide: [programming model](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html) and NVIDIA's [grid-stride loops](https://developer.nvidia.com/blog/cuda-pro-tip-write-flexible-kernels-grid-stride-loops/) | Global index, global stride, bounds, and why launch size need not equal data size |
| 02 | CUDA Programming Guide: [thread hierarchy](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html#thread-hierarchy) | Map block/thread coordinates to `(x, y)` and then to a row-major address |
| 03 | NVIDIA: [using shared memory](https://developer.nvidia.com/blog/using-shared-memory-cuda-cc/) and Mark Harris's [reduction slides](https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf) | Block-local storage, barrier participation, partial blocks, and one partial result per block |
| 04 | CUDA Programming Guide: [atomics](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html#atomics) | Atomicity makes an update indivisible; it does not eliminate serialization under contention |
| 05 | NVIDIA: [finite-difference stencil, Part 1](https://developer.nvidia.com/blog/finite-difference-methods-cuda-cc-part-1/) | Neighborhood geometry, halos, repeated loads, and boundary handling |

Each leaf README narrows the reading and supplies a before-coding check.

The order matters. Do not optimize a failing kernel, and do not copy a finished
kernel from elsewhere. For each lab:

1. Draw the grid and predict which elements two boundary threads own.
2. Implement the smallest correct kernel in the marked region.
3. Test the default awkward input size, then at least `1`, `block_size - 1`,
   `block_size`, and `block_size + 1` where the lab accepts a size argument.
4. Write down one bug and the invariant that fixed it.
5. Record a Release-build timing only after correctness passes.

## Optional companions, in order

The repository labs are self-contained. If a second explanation helps, use one
companion and return to code:

1. [GPU Puzzles](https://github.com/srush/GPU-Puzzles) for visual indexing and
   shared-memory intuition before Labs 01–03.
2. NVIDIA's [accelerated-computing learning path](https://www.nvidia.com/en-us/learn/learning-path/accelerated-computing/)
   if you want a guided CUDA C/C++ weekend.
3. *Programming Massively Parallel Processors*: type the data-parallelism,
   hierarchy, memory, reduction, and convolution examples alongside Labs 01–05.

External certificates are not completion gates; passing correctness checks and
explaining your measurements are.

## Configure and build

Requirements for GPU work are CMake 3.24+, a C++17 compiler, and a CUDA toolkit
supported by the installed NVIDIA driver.

```sh
cmake -S 05_cuda -B build/05_cuda -DCMAKE_BUILD_TYPE=Release
cmake --build build/05_cuda --config Release --parallel
```

CMake targets are named `cuda_vector_add`, `cuda_indexing_2d`,
`cuda_reduction`, `cuda_histogram`, and `cuda_box_blur`. With a multi-config
generator (Visual Studio), executables normally appear below `Release/`.

The default architecture is the GPU installed on the build machine. The two lab
GPUs straddle a toolkit support boundary:

- GTX 1080 is Pascal compute capability 6.1, so use `61` / `sm_61` and a CUDA
  12.x toolkit. CUDA 13 removed offline compilation and library support for
  Pascal.
- RTX 5060 Ti is Blackwell compute capability 12.0, so use `120` / `sm_120` and
  CUDA 12.8 or newer.
- CUDA 12.8 and 12.9 are the overlap releases that can compile both targets.
  CUDA 13 can be used for the RTX machine, but not to build the GTX executable.

Confirm what the installed compiler accepts with `nvcc --list-gpu-code`. The
[NVIDIA compute-capability table](https://developer.nvidia.com/cuda/gpus),
[CUDA 12.8 release notes](https://docs.nvidia.com/cuda/archive/12.8.0/cuda-toolkit-release-notes/index.html),
and [CUDA 13 release notes](https://docs.nvidia.com/cuda/archive/13.0.1/cuda-toolkit-release-notes/index.html)
are the source of truth.

Prefer separate native builds for the comparison:

```sh
cmake -S 05_cuda -B build/05-gtx1080 -DCMAKE_CUDA_ARCHITECTURES=61
cmake -S 05_cuda -B build/05-rtx5060ti -DCMAKE_CUDA_ARCHITECTURES=120
```

You do not need one fat binary for both GPUs. Capture the toolkit and
architecture used by each build in `NOTES.md`.

### No CUDA on this machine

Configuration intentionally succeeds when CUDA is missing. It prints a skip
message and creates only the `cuda_labs_skipped` target. You can force this path
on any machine, which is useful in CPU-only CI:

```sh
cmake -S 05_cuda -B build/05_cuda-no-cuda -DMLSTUDIES_ENABLE_CUDA=OFF
cmake --build build/05_cuda-no-cuda
python 05_cuda/tests/validate_course.py
```

The Python validator is static; it neither imports CUDA packages nor needs a
GPU. A configured CUDA executable still requires an NVIDIA GPU and working
driver at run time. If `cmake` itself is not installed, configuration/building
is impossible, but the Python validator still runs and clearly limits its claim
to course structure. On a toolkit-only host with no visible GPU, force the
`MLSTUDIES_ENABLE_CUDA=OFF` path so native architecture detection is not needed.

## Timing contract

The harnesses use CUDA events, warm up the kernel, synchronize at explicit
boundaries, and report the median of several batches. That number excludes
allocation and host/device transfers. It answers “how long did the kernel take?”
not “how long did the application take?” Chapter 06 adds end-to-end measurements
and profiling. Never compare Debug on one GPU with Release on another.

Keep machine and version facts in [NOTES.md](NOTES.md). In particular, build
separately and natively on the GTX 1080 and RTX 5060 Ti; a single binary or a
single timing sample is not a fair comparison.

## Reflection prompts

- Why is `ceil(n / block_size)` not sufficient without a kernel bounds check?
- Which addresses does a warp touch in your 1-D and 2-D kernels?
- Why does `__syncthreads()` coordinate a block but not an entire grid?
- When does an atomic operation guarantee correctness but still scale poorly?
- Which part of a blur is redundant work that a tile could reuse?
