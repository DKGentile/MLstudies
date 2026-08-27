# Chapter 4: Computer Vision Foundations

This chapter bridges manual array code and a real PyTorch image-classification
run. First, implement convolution and pooling with NumPy so stride, padding,
channels, and output shapes stop being mysterious. Then train a deliberately
small CNN on CIFAR-10 and explain what its curves say.

## Outcomes

By the end, you should be able to:

- compute convolution and pooling output dimensions before running code;
- implement NCHW multi-channel cross-correlation and two pooling operations;
- distinguish kernels, activations, channels, batches, and feature maps;
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
```

On bash/zsh, prefix the command with `RUN_CV_EXERCISES=1`.

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
new machine, in CI, and with the current Python 3.14 environment where a
compatible PyTorch wheel must not be assumed.

## External checkpoint

After the local NumPy exercises, use
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

## Completion gate

You are done when:

- all opt-in convolution/pooling tests pass;
- the PyTorch smoke test reports logits of shape `(batch, 10)` without a data
  download;
- your completed train/evaluation loops can overfit a tiny subset first;
- a full run saves metrics and a best checkpoint; and
- `cifar10/EXPERIMENT_LOG.md` contains at least two controlled runs and a
  five-sentence explanation of the train/validation curves.

The CS231n checkpoint is part of the original 26-week curriculum. If time is short,
finish the repository-native tests and PyTorch experiment first, then slip the
calendar rather than copying assignment answers.

Reference reading from the curriculum:

- [CS231n convolutional-network notes](https://cs231n.github.io/convolutional-networks/)
- [CS231n transfer-learning notes](https://cs231n.github.io/transfer-learning/)
