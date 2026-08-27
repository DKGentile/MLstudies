# Detector Training Lab

Training is an experiment, not a ceremony. Begin with a pre-trained nano detector
and a small input size that leaves room for the deployment target.

## Baseline

```powershell
python train/train_detector.py `
  --model yolov8n.pt `
  --data path/to/dataset.yaml `
  --epochs 50 --imgsz 416 --batch 16 --device 0 `
  --name baseline
```

Model names evolve. `--model` is explicit so you can use a compatible small model
without rewriting the training code. Record its SHA-256 hash and package version.

## Required experiments

Run only after stating a hypothesis:

1. Baseline at fixed seed and split.
2. One overfit diagnostic on a tiny subset.
3. One data or augmentation change motivated by observed failure cases.
4. One input-size comparison relevant to the Nano memory/latency budget.

For every run, save train/validation curves, best checkpoint hash, config, elapsed
time, peak VRAM, per-class metrics, and a one-paragraph conclusion. Do not tune on
the test split.

