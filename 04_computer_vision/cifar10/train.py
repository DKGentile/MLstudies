#!/usr/bin/env python3
"""Safe-by-default starter for a small CIFAR-10 PyTorch experiment.

Running this file without flags only prints the lab plan. ``--smoke-test`` uses
synthetic tensors for one forward pass. Dataset access and optimization happen
only after the explicit ``--train`` flag.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any


LAB_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = LAB_ROOT / "data"
DEFAULT_OUTPUT_DIR = LAB_ROOT / "artifacts"


class DependencyError(RuntimeError):
    """Raised when an explicitly requested mode lacks an optional dependency."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train a small CIFAR-10 CNN, with a download-free smoke mode.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--smoke-test",
        action="store_true",
        help="run one synthetic forward pass; never download or optimize",
    )
    mode.add_argument(
        "--train",
        action="store_true",
        help="run the learner-completed training pipeline",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="allow torchvision to download CIFAR-10 (valid only with --train)",
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--momentum", type=float, default=0.9)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument(
        "--device",
        choices=("auto", "cpu", "cuda"),
        default="auto",
        help="execution device; auto chooses CUDA only when available",
    )
    parser.add_argument(
        "--augment",
        action="store_true",
        help="add random crop and horizontal flip to the training transform",
    )
    return parser


def import_pytorch(*, include_torchvision: bool) -> tuple[Any, Any, Any | None]:
    """Import optional ML packages only after the user requests a run mode."""

    try:
        torch = importlib.import_module("torch")
        nn = importlib.import_module("torch.nn")
    except (ImportError, OSError) as error:
        raise DependencyError(
            "PyTorch is unavailable in this interpreter. Follow cifar10/README.md "
            "and the official PyTorch install selector before using this mode."
        ) from error

    torchvision = None
    if include_torchvision:
        try:
            torchvision = importlib.import_module("torchvision")
        except (ImportError, OSError) as error:
            raise DependencyError(
                "torchvision is unavailable or incompatible with torch. Install a "
                "matching pair using the official PyTorch install selector."
            ) from error
    return torch, nn, torchvision


def seed_everything(torch: Any, seed: int) -> None:
    """Seed CPU and available CUDA generators for repeatable course runs."""

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def resolve_device(torch: Any, requested: str) -> Any:
    """Resolve ``auto`` and reject an unavailable explicitly requested CUDA."""

    if requested == "cuda" and not torch.cuda.is_available():
        raise ValueError("--device cuda was requested, but torch reports no CUDA device")
    selected = "cuda" if requested == "auto" and torch.cuda.is_available() else requested
    if selected == "auto":
        selected = "cpu"
    return torch.device(selected)


def build_model(torch: Any, nn: Any) -> Any:
    """Return the supplied baseline CNN.

    The model is deliberately modest so the lab focuses on a correct experiment
    loop. After establishing a baseline, changing one architectural factor is a
    learner extension.
    """

    class TinyCnn(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(3, 32, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2),
                nn.Conv2d(32, 64, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2),
            )
            self.classifier = nn.Sequential(
                nn.Flatten(),
                nn.Linear(64 * 8 * 8, 128),
                nn.ReLU(),
                nn.Dropout(p=0.25),
                nn.Linear(128, 10),
            )

        def forward(self, inputs: Any) -> Any:
            return self.classifier(self.features(inputs))

    return TinyCnn()


def build_synthetic_loader(torch: Any, *, batch_size: int = 8, seed: int = 0) -> Any:
    """Build one deterministic CIFAR-shaped batch without torchvision or I/O."""

    data = importlib.import_module("torch.utils.data")
    generator = torch.Generator().manual_seed(seed)
    images = torch.randn(batch_size, 3, 32, 32, generator=generator)
    labels = torch.randint(0, 10, (batch_size,), generator=generator)
    dataset = data.TensorDataset(images, labels)
    return data.DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=0)


def build_cifar_loaders(
    torch: Any,
    torchvision: Any,
    *,
    data_dir: Path,
    batch_size: int,
    workers: int,
    seed: int,
    download: bool,
    augment: bool,
) -> tuple[Any, Any]:
    """Build a deterministic 45k/5k split from the CIFAR-10 training set."""

    transforms = torchvision.transforms
    normalize = transforms.Normalize(
        mean=(0.4914, 0.4822, 0.4465),
        std=(0.2470, 0.2435, 0.2616),
    )
    evaluation_transform = transforms.Compose([transforms.ToTensor(), normalize])
    training_steps: list[Any] = []
    if augment:
        training_steps.extend(
            [transforms.RandomCrop(32, padding=4), transforms.RandomHorizontalFlip()]
        )
    training_steps.extend([transforms.ToTensor(), normalize])
    training_transform = transforms.Compose(training_steps)

    training_view = torchvision.datasets.CIFAR10(
        root=str(data_dir),
        train=True,
        transform=training_transform,
        download=download,
    )
    validation_view = torchvision.datasets.CIFAR10(
        root=str(data_dir),
        train=True,
        transform=evaluation_transform,
        download=False,
    )

    data = importlib.import_module("torch.utils.data")
    split_generator = torch.Generator().manual_seed(seed)
    ordering = torch.randperm(len(training_view), generator=split_generator).tolist()
    validation_count = 5_000
    if len(ordering) <= validation_count:
        raise ValueError("CIFAR-10 training set is unexpectedly too small for the split")
    validation_indices = ordering[:validation_count]
    training_indices = ordering[validation_count:]
    train_subset = data.Subset(training_view, training_indices)
    validation_subset = data.Subset(validation_view, validation_indices)

    loader_generator = torch.Generator().manual_seed(seed)
    loader_kwargs = {
        "batch_size": batch_size,
        "num_workers": workers,
        "pin_memory": bool(torch.cuda.is_available()),
    }
    train_loader = data.DataLoader(
        train_subset,
        shuffle=True,
        generator=loader_generator,
        **loader_kwargs,
    )
    validation_loader = data.DataLoader(validation_subset, shuffle=False, **loader_kwargs)
    return train_loader, validation_loader


def train_one_epoch(
    model: Any,
    loader: Any,
    loss_function: Any,
    optimizer: Any,
    device: Any,
) -> dict[str, float]:
    """Train for one epoch and return sample-weighted loss and accuracy."""

    # TODO:
    # 1. put the model in training mode;
    # 2. transfer each input/label batch to device;
    # 3. clear gradients, compute logits/loss, backpropagate, and step;
    # 4. accumulate loss weighted by batch size and count correct predictions;
    # 5. return {"loss": ..., "accuracy": ...} over every seen sample.
    raise NotImplementedError("implement train_one_epoch")


def evaluate(
    model: Any,
    loader: Any,
    loss_function: Any,
    device: Any,
    torch: Any,
) -> dict[str, float]:
    """Evaluate without optimization and return loss plus accuracy."""

    # TODO: mirror the measurement logic in train_one_epoch, but switch the
    # model to evaluation mode and disable gradient tracking for the whole loop.
    # There must be no optimizer operation here.
    raise NotImplementedError("implement evaluate")


def save_curves(history: dict[str, list[float]], output_path: Path) -> None:
    """Save labeled train/validation loss and accuracy curves to one PNG."""

    # TODO: import matplotlib.pyplot locally, plot loss and accuracy against
    # 1-based epoch numbers, label every axis/series, and close the figure after
    # saving it to output_path. Create no interactive window.
    raise NotImplementedError("implement save_curves")


def run_smoke_test(torch: Any, nn: Any, *, requested_device: str, seed: int) -> None:
    """Perform exactly one synthetic forward pass and print a compact report."""

    seed_everything(torch, seed)
    device = resolve_device(torch, requested_device)
    loader = build_synthetic_loader(torch, batch_size=8, seed=seed)
    model = build_model(torch, nn).to(device)
    model.eval()
    images, _ = next(iter(loader))
    with torch.no_grad():
        logits = model(images.to(device))
    if tuple(logits.shape) != (8, 10):
        raise RuntimeError(f"expected logits shape (8, 10), received {tuple(logits.shape)}")
    if not bool(torch.isfinite(logits).all().item()):
        raise RuntimeError("smoke-test logits contain a non-finite value")
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    print(
        f"Smoke test passed: device={device}, logits={tuple(logits.shape)}, "
        f"parameters={parameter_count:,}; no data downloaded and no optimizer step run."
    )


def run_training(torch: Any, nn: Any, torchvision: Any, args: argparse.Namespace) -> None:
    """Construct the requested run and orchestrate learner-completed functions."""

    seed_everything(torch, args.seed)
    device = resolve_device(torch, args.device)
    train_loader, validation_loader = build_cifar_loaders(
        torch,
        torchvision,
        data_dir=args.data_dir,
        batch_size=args.batch_size,
        workers=args.workers,
        seed=args.seed,
        download=args.download,
        augment=args.augment,
    )
    model = build_model(torch, nn).to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=args.learning_rate,
        momentum=args.momentum,
        weight_decay=args.weight_decay,
    )
    history: dict[str, list[float]] = {
        "train_loss": [],
        "train_accuracy": [],
        "validation_loss": [],
        "validation_accuracy": [],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    best_validation_loss = float("inf")

    for epoch in range(1, args.epochs + 1):
        training = train_one_epoch(model, train_loader, loss_function, optimizer, device)
        validation = evaluate(model, validation_loader, loss_function, device, torch)
        history["train_loss"].append(training["loss"])
        history["train_accuracy"].append(training["accuracy"])
        history["validation_loss"].append(validation["loss"])
        history["validation_accuracy"].append(validation["accuracy"])
        print(
            f"epoch={epoch:02d} "
            f"train_loss={training['loss']:.4f} train_acc={training['accuracy']:.3f} "
            f"val_loss={validation['loss']:.4f} val_acc={validation['accuracy']:.3f}"
        )
        if validation["loss"] < best_validation_loss:
            best_validation_loss = validation["loss"]
            torch.save(
                {
                    "model_state": model.state_dict(),
                    "epoch": epoch,
                    "validation_loss": validation["loss"],
                    "args": vars(args),
                },
                args.output_dir / "best_checkpoint.pt",
            )
        (args.output_dir / "metrics.json").write_text(
            json.dumps(history, indent=2), encoding="utf-8"
        )

    save_curves(history, args.output_dir / "curves.png")
    print(f"Artifacts saved under {args.output_dir.resolve()}")


def validate_arguments(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.download and not args.train:
        parser.error("--download is valid only together with --train")
    if args.epochs <= 0:
        parser.error("--epochs must be positive")
    if args.batch_size <= 0:
        parser.error("--batch-size must be positive")
    if args.learning_rate <= 0.0:
        parser.error("--learning-rate must be positive")
    if args.momentum < 0.0:
        parser.error("--momentum cannot be negative")
    if args.weight_decay < 0.0:
        parser.error("--weight-decay cannot be negative")
    if args.workers < 0:
        parser.error("--workers cannot be negative")


def print_plan() -> None:
    print(
        "CIFAR-10 lab is idle (safe default).\n"
        "  1. Read cifar10/README.md and install a compatible PyTorch build.\n"
        "  2. Run this file with --smoke-test for one synthetic forward pass.\n"
        "  3. Implement the three TODO functions.\n"
        "  4. Use --train; add --download only when data acquisition is intended.\n"
        "No PyTorch import, download, training, or file write was performed."
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_arguments(parser, args)

    if not args.smoke_test and not args.train:
        print_plan()
        return 0

    try:
        torch, nn, torchvision = import_pytorch(include_torchvision=args.train)
        if args.smoke_test:
            run_smoke_test(torch, nn, requested_device=args.device, seed=args.seed)
        else:
            run_training(torch, nn, torchvision, args)
    except (DependencyError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except NotImplementedError as error:
        print(
            f"exercise incomplete: {error}. Read cifar10/README.md and search train.py for TODO.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
