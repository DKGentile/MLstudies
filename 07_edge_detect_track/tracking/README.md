# Tracking Extensions: From IoU Baseline to SORT and ByteTrack

## Prepare

Use this order so the papers explain observed failures rather than becoming code
templates:

1. Implement and break the local IoU baseline on synthetic sequences.
2. Read MIT's [Kalman-filter notes](https://ocw.mit.edu/courses/2-160-identification-estimation-and-learning-spring-2006/resources/lecture_5/)
   and write your state, transition, observation, and uncertainty assumptions.
3. Read SciPy's [`linear_sum_assignment`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html)
   contract; construct the cost matrix and gating rules yourself.
4. Compare the result with the original [SORT paper](https://arxiv.org/abs/1602.00763).
5. Only after low-confidence detections cause visible fragmentation, read
   [ByteTrack](https://arxiv.org/abs/2110.06864).

Extension after you have labeled identities: the [HOTA paper](https://arxiv.org/abs/2009.07736)
separates detection, association, and localization quality.

Complete the simple IoU tracker first. Its failures make the extra machinery in
SORT easier to justify.

## Lab 1 — Motion prediction

Implement and test `ConstantVelocityKalman1D` in
`src/edge_course/kalman.py`. Plot noisy measurements, predictions, and posterior
estimates for a synthetic constant-velocity target. Then deliberately introduce an
acceleration and explain the lag.

Extend the idea to bounding boxes. State your chosen vector explicitly. A common
design tracks center coordinates plus scale/height and aspect ratio, with velocity
terms for the components assumed to move. Test conversions between `xyxy` and the
filter state independently from filtering.

## Lab 2 — Global assignment

The supplied greedy counterexample proves local choices can lose valid matches.
Replace greedy matching with a Hungarian/linear-sum assignment using a cost derived
from IoU. Add tests for:

- the counterexample in `test_matching.py`;
- forbidden class-mismatched pairs;
- tracks/detections with no eligible partner;
- a rectangular cost matrix; and
- deterministic behavior under ties.

You may use a trusted assignment implementation in the capstone after you can
explain the cost matrix and gating. Keep the greedy baseline for comparison.

## Lab 3 — Full SORT behavior

Predict every track before association, match detections, update matched filters,
and manage `age`, `hits`, and `missed` state. Do not display tentative tracks until
they reach a documented hit threshold. Build three synthetic sequences: crossing
objects, short occlusion, and a large camera jump.

Revisit the original SORT paper after your baseline fails those cases and list
which state and lifecycle choices in your implementation differ.

## Lab 4 — ByteTrack-style second association

Partition detections into high- and low-confidence sets. Match active tracks to
high-confidence detections first, then give unmatched tracks a second association
against low-confidence detections. Measure whether this reduces fragmentation and
whether it increases false continuation on your validation sequences.

The goal is not to claim a faithful ByteTrack reproduction from this short lab.
Compare your design to the paper and name every simplification.

## Evaluate tracking, not only detection

Label a small but representative sequence with persistent object identities. Report
at least track recall, ID switches, and fragmentation count; optionally use a
standard evaluator for IDF1/HOTA. Show per-sequence results and failure clips.
Detection mAP alone cannot establish tracker quality.
