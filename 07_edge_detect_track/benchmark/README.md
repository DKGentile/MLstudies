# Benchmark Harness

## Prepare

Read TensorRT's official [benchmarking guidance](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html)
for warmup, synchronization, throughput, and latency definitions. Use the
[Nsight Systems guide](https://docs.nvidia.com/nsight-systems/UserGuide/) when the
question spans CPU work, copies, kernels, and idle gaps rather than one kernel.

Before measuring, write a one-sentence boundary such as "preallocated model
execution from synchronized input-ready to synchronized output-ready." A timing
number without its boundary, device state, input shape, precision, and summary
statistic is not comparable evidence.

Use [latency.py](latency.py) inside each runtime adapter. Its synchronization hook
is mandatory for asynchronous GPU APIs.

Minimum protocol:

- fix input shape, batch, precision, and power mode;
- run at least 20 warmups and 200 measured iterations;
- synchronize immediately before starting and after each operation under test;
- report median, p95, p99, mean, and standard deviation;
- validate outputs before trusting speed;
- record temperature/clocks if throttling is plausible;
- benchmark model-only and end-to-end paths separately.

Use `results/benchmark.template.csv` for the summary and keep raw samples or the
script that regenerates them.
