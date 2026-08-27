# Benchmark Harness

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

