# Dataset Audit Lab

Do this before training. A detector can produce plausible curves while learning a
duplicate-heavy or leaked split.

## Required checks

- Record source URL, version/date, license, and any use restrictions. Separately
  record the model-weight and training/deployment framework licenses; they are not
  implied by the dataset license.
- Count images, boxes, and boxes per class for every split.
- Validate that normalized YOLO coordinates are finite and inside `[0, 1]`.
- Find missing labels, missing images, empty label files, invalid class IDs, and
  zero-area boxes.
- Hash image bytes and report exact duplicates crossing train/validation/test.
- Plot class balance and bounding-box width/height/area distributions.
- Manually inspect at least 50 random annotated images.

Implement `validate_yolo_row` in [audit_yolo.py](audit_yolo.py), then extend the CLI
to emit a JSON report for your chosen dataset.

```powershell
python -m pytest tests/test_dataset_audit.py -q
python dataset/audit_yolo.py --labels path/to/labels --num-classes 3
```

## Split questions

If video frames are adjacent in time, a random per-frame split leaks nearly
identical scenes. Split by video, recording session, camera, or location. Write the
unit of independence in your experiment report.
