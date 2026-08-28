# Dataset Audit Lab

## Prepare

Required before choosing or splitting data:

- Read the question categories in [Datasheets for Datasets](https://arxiv.org/abs/1803.09010).
  Use them to record provenance, collection conditions, intended use, license,
  and known gaps; do not fill the report with guessed answers.
- Read the Ultralytics [detection dataset format](https://docs.ultralytics.com/datasets/detect)
  for the exact class and normalized `xywh` label contract.
- Read the contract for scikit-learn's [`GroupShuffleSplit`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html).
  The important idea is group-level independence, not whether you use that class.

Before coding, name the real independent unit in your data: video, session,
camera, site, subject, or something else. A random frame split is not defensible
when adjacent frames show effectively the same event.

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
