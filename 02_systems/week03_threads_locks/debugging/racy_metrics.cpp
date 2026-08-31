#include <atomic>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <thread>
#include <vector>

namespace {

// This file is intentionally incorrect. It models shared counters that a
// network receiver and worker pool might update. Do not copy this design into
// the real pipeline.
struct PipelineMetrics {
  std::uint64_t frames_processed = 0;
  std::uint64_t bytes_processed = 0;
};

void record_frame_with_intentional_race(PipelineMetrics& metrics,
                                        std::size_t bytes) {
  // INTENTIONAL DATA RACE CLINIC: multiple workers execute both operations.
  ++metrics.frames_processed;
  metrics.bytes_processed += bytes;
}

}  // namespace

int main() {
  constexpr std::size_t worker_count = 4;
  constexpr std::size_t frames_per_worker = 100000;
  constexpr std::size_t bytes_per_frame = 4096;

  PipelineMetrics metrics;
  std::atomic<std::size_t> ready{0};
  std::atomic<bool> start{false};
  std::vector<std::thread> workers;
  workers.reserve(worker_count);

  for (std::size_t worker = 0; worker < worker_count; ++worker) {
    workers.emplace_back([&] {
      ready.fetch_add(1, std::memory_order_release);
      while (!start.load(std::memory_order_acquire)) {
        std::this_thread::yield();
      }
      for (std::size_t frame = 0; frame < frames_per_worker; ++frame) {
        record_frame_with_intentional_race(metrics, bytes_per_frame);
      }
    });
  }

  while (ready.load(std::memory_order_acquire) != worker_count) {
    std::this_thread::yield();
  }
  start.store(true, std::memory_order_release);

  for (auto& worker : workers) {
    worker.join();
  }

  const auto expected_frames = worker_count * frames_per_worker;
  const auto expected_bytes = expected_frames * bytes_per_frame;
  std::cout << "expected_frames=" << expected_frames << '\n'
            << "observed_frames=" << metrics.frames_processed << '\n'
            << "expected_bytes=" << expected_bytes << '\n'
            << "observed_bytes=" << metrics.bytes_processed << '\n';
  std::cout << "A numerically correct run would not make the accesses safe.\n";
  return 0;
}
