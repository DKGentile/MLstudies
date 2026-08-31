# Chapter 4: Computer Vision Foundations

This chapter bridges manual array code, geometric image formation, and a real
PyTorch image-classification run. Implement convolution and pooling with NumPy
so stride, padding, channels, and output shapes stop being mysterious. Train a
deliberately small CNN on CIFAR-10 and explain what its curves say. Then build a
compact camera-geometry toolkit so later perception work has explicit frames,
transforms, projection, and inverse-ray reasoning beneath it.

## Outcomes

By the end, you should be able to:

- compute convolution and pooling output dimensions before running code;
- implement NCHW multi-channel cross-correlation and two pooling operations;
- distinguish kernels, activations, channels, batches, and feature maps;
- distinguish points from vectors and compose/invert named 2-D and 3-D rigid
  frame transforms;
- derive pinhole projection from intrinsics and world-to-camera extrinsics;
- map pixels to normalized camera coordinates and unit rays while explaining
  why a pixel alone does not recover depth;
- smoke-test a CNN using synthetic tensors without network access;
- write a correct PyTorch train/evaluation loop and save a checkpoint; and
- use train/validation curves to recognize optimization trouble and overfit.

## Core setup

The NumPy primitives and their tests do not require PyTorch:

```powershell
python -m pip install -r 04_computer_vision/requirements.txt
python -m pytest 04_computer_vision/tests -q
```

Challenge tests are opt-in. In PowerShell:

```powershell
$env:RUN_CV_EXERCISES = "1"
python -m pytest 04_computer_vision/tests/test_conv_pool.py -q
python -m pytest 04_computer_vision/tests/test_camera_geometry.py -q
```

On bash/zsh, prefix the command with `RUN_CV_EXERCISES=1`.

## Preparation at the point of use

Use the **core** source before the corresponding code and the **extension** only
after a first implementation. The external APIs are useful as independent
contracts and oracles; the local docstrings and tests decide this chapter's exact
behavior.

| Stage | Core before coding | Ready-to-code check | Extension after first attempt |
|---|---|---|---|
| NumPy convolution and pooling | Read the “Convolutional Layer,” “Pooling Layer,” and output-size portions of Stanford's [CS231n convolutional-network notes](https://cs231n.github.io/convolutional-networks/). | Derive `H_out` and `W_out` from input, kernel, padding, and stride. State the filter shape for NCHW data, and explain why the operation here is cross-correlation. | Treat PyTorch's [`conv2d`](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.conv2d.html), [`max_pool2d`](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.max_pool2d.html), and [`avg_pool2d`](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.avg_pool2d.html) as comparison oracles on small random cases. Do not replace the required NumPy implementation with them. |
| CIFAR-10 training | Complete the loop preparation in the [CIFAR-10 lab](cifar10/README.md) immediately before editing its TODOs. | Explain the training/evaluation mode difference, gradient lifecycle, whole-dataset metric aggregation, and checkpoint criterion. | After one correct epoch and a tiny-subset overfit, use the lab's reproducibility and experiment resources to interpret curves. |
| Camera geometry and coordinate frames | Study Northwestern's concise [homogeneous-transformation lesson](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/), then read the camera-matrix sections of Stanford CS231A's [Camera Models notes](https://web.stanford.edu/class/cs231a/course_notes/01-camera-models.pdf). | Given `T_A_B` and `T_B_C`, state the direction and order of `T_A_C`; derive the rigid inverse and `u = fx X/Z + cx`, `v = fy Y/Z + cy`; explain why `T_C_W` is not the camera pose. | Compare a completed NumPy projection with OpenCV's official [`calib3d` camera model](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html) and optionally `cv2.projectPoints` if OpenCV is already installed. Keep distortion zero and match frame conventions; do not add OpenCV as a requirement or replace the exercise with it. |
| Stanford checkpoint | Read each official assignment page only when you reach its listed section in [CS231N_CHECKPOINT.md](CS231N_CHECKPOINT.md). | Write down tensor shapes, the slowest avoidable loop, and the expected gradient-check target before each section. | Compare controlled results with the repository-native implementation; do not move solution code between the two projects. |

## Part 1: convolution and pooling primitives

Work in `computer_vision/conv_pool.py`. This chapter uses these conventions:

- images/activations: `(batch, input_channels, height, width)`;
- filters: `(output_channels, input_channels, kernel_height, kernel_width)`;
- bias: one scalar per output channel;
- `conv2d_nchw` performs cross-correlation, as deep-learning libraries do (the
  kernel is not spatially flipped);
- stride and symmetric zero-padding are scalar integers in this exercise; and
- output size uses floor semantics.

Suggested progression:

1. Calculate each output shape on paper.
2. Implement a clear nested-loop reference version.
3. Pass the identity, channel-mixing, stride, and padding tests.
4. Compare a few random cases against `torch.nn.functional.conv2d` if PyTorch
   is available.
5. Only as an optional extension, vectorize with strided windows or `im2col`.

Correctness is the goal. A compact but opaque vectorization is not an upgrade
until it is tested against a simple reference.

## Part 2: CIFAR-10 training lab

Continue with [the CIFAR-10 lab](cifar10/README.md). Its entrypoint is safe by
default:

```powershell
python 04_computer_vision/cifar10/train.py
```

That command prints instructions and exits. It does not import PyTorch, create
files, download data, or train. Once a compatible PyTorch installation exists,
this command performs one synthetic forward pass only:

```powershell
python 04_computer_vision/cifar10/train.py --smoke-test --device cpu
```

Actual CIFAR-10 access and training require explicit flags. This matters on a
new machine or in CI, where a compatible PyTorch installation must not be
assumed merely because Python is present.

## Part 3: camera geometry and coordinate frames

Work in `computer_vision/camera_geometry.py`. The exercise uses batched row
arrays in Python, but write the mathematics with column vectors and explicit
frame names. The central convention is:

Prepare the frame notation during Week 8 and implement this focused lab in Week
9 alongside CUDA launch geometry. Keep the capstone problem statement moving in
parallel; camera geometry does not postpone its Week 10 dataset audit.

```text
p_A = T_A_B p_B
T_A_C = T_A_B T_B_C
p ~ K [R_C_W | t_C_W] P_W
```

`T_A_B` maps coordinates expressed in frame B into frame A. Subscripts cancel
when transforms are composed in the correct order. For the camera equation,
`T_C_W = [R_C_W | t_C_W]` is the world-to-camera extrinsic. The camera pose in
the world is `T_W_C`, its inverse. The `~` symbol means equality up to a nonzero
homogeneous scale; recovering `(u, v)` requires a perspective divide.

Use these remaining conventions consistently:

- points have homogeneous coordinate one, while free vectors/directions have
  homogeneous coordinate zero, so a translation changes only points;
- proper 2-D and 3-D rotations are orthonormal and have determinant `+1`;
- the right-handed camera frame uses `+X` right, `+Y` down, and `+Z` forward,
  and only strictly positive camera depth is projectable by this lab;
- pixel coordinates are `(u, v)` in column-row order, not NumPy's `(row,
  column)` indexing order;
- `K` is the zero-skew pinhole intrinsic matrix with focal lengths `(fx, fy)`
  in pixels and principal point `(cx, cy)`; and
- normalized camera coordinates `(x_n, y_n)` and a unit camera ray are related
  but are not the same object.

Implement in three passes:

1. Homogenize/dehomogenize points and vectors. Construct one SE(2) transform by
   hand and prove with a numerical example that translation does not affect a
   vector.
2. Construct, apply, compose, and invert rigid transforms. Use names such as
   `T_A_B` in notes and code; do not use `np.linalg.inv` for a rigid inverse.
3. Construct `K`, project camera- and world-frame points, undo `K` to obtain
   normalized coordinates, and produce unit rays. Check the principal point,
   an off-axis point, positive depth-scale invariance, and invalid depth before
   trying random data.

Run only this challenge while working on it:

```powershell
$env:RUN_CV_EXERCISES = "1"
python -m pytest 04_computer_vision/tests/test_camera_geometry.py -q
```

The tests intentionally require a whole projection call to reject a batch if
even one point has `Z <= 0`. This fail-fast contract avoids silently treating a
point on or behind the camera plane as a valid pixel. A production point-cloud
pipeline may explicitly build a positive-depth mask before projection, but it
must make that policy visible rather than relying on infinities or NaNs.

### Calibration and distortion boundary

Camera calibration estimates intrinsics, lens-distortion coefficients, and
per-view extrinsics from known correspondences, commonly observations of a
calibration target. Radial distortion changes displacement as distance from the
optical axis grows (barrel or pincushion behavior); tangential distortion models
lens/sensor misalignment. Neither effect is represented by the ideal matrix `K`
alone. Learn those concepts and inspect OpenCV's model, but do not implement a
calibrator or distortion solver in this compact lab.

Required scope ends at single-camera pinhole projection and rays. Epipolar
geometry, stereo reconstruction, bundle adjustment, visual odometry, SLAM, and
robotics state estimation are deliberately not part of this curriculum pass.

## External checkpoint

During Weeks 5–8, after the local NumPy convolution exercises, use
[CS231n_CHECKPOINT.md](CS231N_CHECKPOINT.md) to complete the public Spring 2026
Assignment 1 and 2 starters. They are not vendored here, and this repository does
not contain solution code.

## Questions to answer in your notes

- Why can convolution preserve width at stride 1 with some odd kernel sizes?
- What work grows when input channels double? What grows when output channels
  double?
- Why does max pooling route a gradient to fewer locations than average
  pooling?
- Why is evaluation run with gradient tracking disabled?
- Why can validation loss rise while validation accuracy stays flat?
- Which change helped generalization most: weight decay, augmentation, model
  size, or early stopping? What evidence supports the claim?
- Why does a translation affect a point but not a free vector?
- If `T_C_W` is known, how do you obtain the camera pose, and why does reversing
  the subscripts reverse the transform?
- Why do all positive points on one camera ray project to the same pixel?
- Which quantities belong to intrinsics, extrinsics, and distortion, and which
  of them change when the camera moves without changing its lens settings?

## Completion gate

You are done when:

- all opt-in convolution/pooling tests pass;
- all opt-in camera-geometry tests pass, including composition, inversion,
  projection, invalid-depth, and pixel-ray cases;
- the PyTorch smoke test reports logits of shape `(batch, 10)` without a data
  download;
- your completed train/evaluation loops can overfit a tiny subset first;
- a full run saves metrics and a best checkpoint;
- `cifar10/EXPERIMENT_LOG.md` contains at least two controlled runs and a
  five-sentence explanation of the train/validation curves; and
- from a blank page, you can label world/camera/pixel frames, derive
  `p ~ K [R | t] P`, distinguish intrinsics from extrinsics, and explain why
  inverse projection yields a ray rather than a unique 3-D point.

The CS231n checkpoint is part of the original 26-week curriculum. If time is short,
finish the repository-native tests and PyTorch experiment first, then slip the
calendar rather than copying assignment answers.
