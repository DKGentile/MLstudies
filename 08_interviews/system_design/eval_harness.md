# Design Prompt — Perception Evaluation Harness

## Prepare

Review COCO's [detection-evaluation page](https://cocodataset.org/#detection-eval)
and [official evaluator contract](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py),
the original [HOTA paper](https://arxiv.org/abs/2009.07736), and the NeurIPS
[paper checklist guidelines](https://neurips.cc/public/guides/PaperChecklist).
Together they cover metric contracts, association-aware tracking evaluation,
dataset/compute disclosure, uncertainty, and reproducibility.

Before designing storage or services, write the immutable identities and the
decision the harness must support. Aggregate metrics alone cannot define a safe
promotion policy when important slices or target hardware regress.

Design an evaluation service that compares candidate detector/tracker builds before
edge deployment. It must handle dataset versions, slice metrics, reproducibility,
and regressions in both accuracy and runtime.

Address:

- immutable dataset/model/runtime identities;
- annotation corrections without rewriting history;
- frame-level detection metrics and sequence-level tracking metrics;
- slices such as night, blur, camera, range, weather, and object size;
- hardware-specific latency runners and noisy measurements;
- acceptance policies with uncertainty and metric tradeoffs;
- artifact lineage, access control, and auditability;
- canary feedback without treating unreviewed production predictions as labels.

Follow-up: the aggregate mAP improves, small-object recall falls 8%, and desktop
latency improves while Nano p95 regresses. Explain who decides and what evidence is
missing.
