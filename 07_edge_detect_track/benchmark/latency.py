"""Reusable synchronous latency sampler for Python inference adapters."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
import statistics
import time
from typing import Any


@dataclass(frozen=True)
class LatencySummary:
    iterations: int
    median_ms: float
    p95_ms: float
    p99_ms: float
    mean_ms: float
    stdev_ms: float


def percentile(samples: list[float], fraction: float) -> float:
    ordered = sorted(samples)
    if not ordered:
        raise ValueError("samples cannot be empty")
    index = min(len(ordered) - 1, max(0, int(round(fraction * (len(ordered) - 1)))))
    return ordered[index]


def measure(
    operation: Callable[[], Any],
    *,
    warmup: int = 20,
    iterations: int = 200,
    synchronize: Callable[[], None] = lambda: None,
) -> tuple[LatencySummary, Any]:
    if warmup < 0 or iterations <= 0:
        raise ValueError("warmup must be non-negative and iterations must be positive")
    last_result: Any = None
    for _ in range(warmup):
        last_result = operation()
        synchronize()
    samples: list[float] = []
    for _ in range(iterations):
        synchronize()
        start = time.perf_counter_ns()
        last_result = operation()
        synchronize()
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        samples.append(elapsed_ms)
    summary = LatencySummary(
        iterations=iterations,
        median_ms=statistics.median(samples),
        p95_ms=percentile(samples, 0.95),
        p99_ms=percentile(samples, 0.99),
        mean_ms=statistics.fmean(samples),
        stdev_ms=statistics.stdev(samples) if len(samples) > 1 else 0.0,
    )
    return summary, last_result


def as_jsonable(summary: LatencySummary) -> dict[str, float | int]:
    return asdict(summary)

