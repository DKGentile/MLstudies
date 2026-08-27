# CIFAR-10 Small-CNN Lab

The starter supplies a tiny baseline CNN, deterministic synthetic smoke data,
safe dataset plumbing, argument parsing, and checkpoint orchestration. You own
the learning-critical pieces: the train loop, evaluation loop, and curve
plotting. Search `train.py` for `TODO`.

## 1. Install PyTorch deliberately

Do not assume the repository's current Python 3.14 interpreter has compatible
PyTorch packages. Check the official [PyTorch install
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

## 3. Implement the learning loops

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

## 4. Acquire data explicitly

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

## 5. Controlled experiments

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
