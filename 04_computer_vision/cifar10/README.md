# CIFAR-10 Small-CNN Lab

The starter supplies a tiny baseline CNN, deterministic synthetic smoke data,
safe dataset plumbing, argument parsing, and checkpoint orchestration. You own
the learning-critical pieces: the train loop, evaluation loop, and curve
plotting. Search `train.py` for `TODO`.

## 1. Install PyTorch deliberately

Do not assume an arbitrary Python/CUDA combination has compatible PyTorch
packages. Check the official [PyTorch install
selector](https://pytorch.org/get-started/locally/) for the Python/CUDA pair on
the target machine. If it does not offer a matching wheel, create a separate
supported Python environment (often Python 3.12 is a practical course
environment) rather than changing the base interpreter.

After selecting the correct PyTorch command, install the remaining optional
lab dependency:

```powershell
python -m pip install matplotlib
```

`requirements-pytorch.txt` is a convenience list, not a substitute for choosing
the correct CUDA wheel/index from the official selector.

Record `python --version`, `torch.__version__`, the CUDA runtime reported by
PyTorch, and the GPU name in `EXPERIMENT_LOG.md`.

## 2. Prove the environment without touching CIFAR-10

```powershell
python 04_computer_vision/cifar10/train.py --smoke-test --device cpu
python 04_computer_vision/cifar10/train.py --smoke-test --device auto
```

Each command creates deterministic synthetic `(3, 32, 32)` tensors and performs
one forward pass. It does not optimize, access the network, or write a
checkpoint. The expected final message includes `(8, 10)` logits.

To make pytest invoke this optional check too:

```powershell
$env:RUN_TORCH_SMOKE = "1"
python -m pytest 04_computer_vision/tests/test_cifar_entrypoint.py -q
```

## 3. Prepare for the learning loops

### Core before coding

Read PyTorch's official [optimization
tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
through its train and test loops, then inspect the framework contracts for
[`Module.train`](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.train),
[`Module.eval`](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval),
and [`torch.no_grad`](https://docs.pytorch.org/docs/stable/generated/torch.no_grad.html).
The official [CIFAR-10 classifier
tutorial](https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial)
shows the same lifecycle in an image-classification setting.

Before editing a TODO, close those pages and write the lifecycle of one batch in
words. Your explanation should account for all of these questions:

- Why are gradients cleared before `backward`, and what would accumulate if they
  were not?
- Which operations belong only in training, and which still belong in evaluation?
- Why are both evaluation mode and disabled gradient tracking needed even though
  neither calls the optimizer?
- If the final batch is smaller, why can averaging per-batch mean losses give the
  wrong whole-dataset mean?
- Which validation quantity selects the best checkpoint, and why must the test set
  not make that choice?

The tutorials demonstrate framework mechanics, not this starter's answer. The
local function signatures, sample-weighted metrics, return values, CLI behavior,
and tests remain authoritative.

### Extension after the first attempt

After one synthetic batch works, use PyTorch's [reproducibility
note](https://docs.pytorch.org/docs/stable/notes/randomness.html) to identify the
sources of variation you can and cannot control. After checkpointing works, compare
it with the official [saving/loading
guide](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html).
Use the creators' [CIFAR-10 page](https://www.cs.toronto.edu/~kriz/cifar.html) for
dataset provenance rather than a third-party summary.

## 4. Implement the learning loops

Fill these functions in `train.py`:

- `train_one_epoch`: training mode, device transfer, clear gradients, forward,
  loss, backward, optimizer step, sample-weighted loss, and accuracy;
- `evaluate`: evaluation mode, disabled gradients, device transfer, loss and
  accuracy, with no optimizer calls; and
- `save_curves`: a labeled train/validation loss and accuracy figure.

Recommended debugging order:

1. one synthetic batch;
2. two batches from a tiny CIFAR subset;
3. deliberately overfit 128 images;
4. only then run the complete train/validation split.

## 5. Acquire data explicitly

The script never downloads implicitly. The first run must opt in:

```powershell
python 04_computer_vision/cifar10/train.py --train --download --epochs 1 --device auto
```

Later runs omit `--download` and reuse the local dataset:

```powershell
python 04_computer_vision/cifar10/train.py --train --epochs 15 --device auto
```

Use `--help` for every option. Data defaults to `cifar10/data/` and generated
artifacts to `cifar10/artifacts/`; both directories are ignored by Git.

## 6. Controlled experiments

Run a baseline, then change one factor at a time. Good first comparisons are:

- no augmentation versus `--augment`;
- weight decay 0 versus `5e-4`;
- default hidden width versus a smaller model you implement; and
- training past the epoch with best validation loss versus stopping there.

Keep the seed fixed when comparing configurations. Copy metrics into
`EXPERIMENT_LOG.md`, preserve the curves, and write at least five sentences:
what overfit, when the evidence appeared, what you changed, what the change did,
and what you would test next.

## Optional extensions

- Add a confusion matrix and inspect the most confused class pair.
- Visualize incorrectly classified images with predicted probabilities.
- Add automatic mixed precision only after the FP32 loop is correct.
- Profile data-loading and GPU utilization before increasing model size.
- Export the trained model to ONNX in a later deployment chapter.
