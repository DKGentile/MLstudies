# Python Inference Pipeline

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

