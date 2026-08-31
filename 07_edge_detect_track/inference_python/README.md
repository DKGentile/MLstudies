# Python Inference Pipeline

## Prepare

Read OpenCV's [geometric image transformations](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html)
for coordinate conventions and interpolation, then review the chosen detector's
documented input/output contract. Keep the local tests—not a framework helper—as
the specification for `letterbox` and inverse box mapping.

Before coding, write the affine mapping from original coordinates to resized,
padded coordinates and its inverse. Record scale and both padding offsets; test
odd padding and non-square images before attaching a model.

This is a 2-D image-plane coordinate transform, not a pinhole-camera extrinsic.
Review Chapter 04's camera-frame notation if you cannot state why letterbox
metadata does not determine camera pose, focal length, or a 3-D point's depth.

Use the Python path to establish correctness and stage-level timings before taking
on TensorRT C++ integration.

Implement `letterbox` and `scale_boxes_back` in [preprocess.py](preprocess.py).
Their tests use synthetic images and require only NumPy.

Then build a thin adapter around your chosen detector with this interface:

```python
class Detector:
    def predict(self, image_bgr) -> list[Detection]: ...
```

Your pipeline loop should:

1. decode one frame;
2. preprocess with recorded geometry;
3. run the detector;
4. map boxes back to original coordinates;
5. update `IoUTracker`;
6. render or serialize results;
7. time each stage after warmup.

Start with a prerecorded video so results are reproducible. Add live camera input
only after the file path works.
