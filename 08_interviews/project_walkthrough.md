# Capstone Walkthrough Drill

Practice three versions: 90 seconds, 5 minutes, and 15 minutes.

## Narrative spine

1. Operational goal and constraints.
2. Why this dataset/model/input size was a sensible baseline.
3. Architecture from frame to track output.
4. One evaluation discovery that changed the work.
5. One measured performance bottleneck and intervention.
6. Desktop versus Nano compatibility/deployment decision.
7. Known failure modes and the next experiment.

## Questions you must answer from your own artifacts

- How was the split constructed, and where could leakage remain?
- What exactly does your mAP implementation/tool compute?
- Why does a confidence threshold move precision and recall?
- When does IoU-only tracking fail? Why would a motion model help?
- Which latency number includes decode, NMS, tracking, and rendering?
- Where do host/device copies and synchronizations happen?
- Why is an engine rebuilt per target?
- What evidence shows FP16 did not materially change outputs?
- What would fail first with four video streams?
- What did you intentionally leave unfinished?

