# Export and Parity Lab

An export is complete only when the exported graph produces acceptable outputs on
representative inputs.

## Export

```powershell
python export/export_model.py --model path/to/best.pt --imgsz 416 --opset 17
```

The script uses the framework's supported ONNX exporter and prints its versions and
arguments. Preserve the `.pt` hash, output ONNX hash, opset, static/dynamic shape,
and simplification flags in the experiment report.

## Parity protocol

1. Freeze 20 representative preprocessed inputs, including edge cases.
2. Capture raw framework outputs before NMS.
3. Run the same arrays through ONNX Runtime.
4. Match output names/shapes, then report max absolute and relative error.
5. Separately compare decoded boxes/classes after postprocessing.

Do not compare two pipelines that resize or normalize differently and call the
result “model drift.” First compare the exact tensor entering the model.

## TensorRT rule

Move the ONNX file—not a desktop `.engine`—to another target. Build and benchmark a
new engine on that target using its installed TensorRT. Record the exact `trtexec`
command and logs.

