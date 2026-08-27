#pragma once

#include <cstddef>
#include <vector>

namespace systems_course::week04 {

struct Frame {
  std::size_t sequence = 0;
  std::vector<int> samples;
};

struct FrameResult {
  std::size_t sequence = 0;
  long long peak_to_peak = 0;
};

inline bool operator==(const FrameResult& left, const FrameResult& right) {
  return left.sequence == right.sequence &&
         left.peak_to_peak == right.peak_to_peak;
}

struct PipelineReport {
  std::size_t worker_count = 0;
  std::size_t queue_capacity = 0;
  std::vector<FrameResult> results;
};

// Processes every input exactly once using worker_count threads and a bounded
// queue of queue_capacity. Results preserve input order. Empty sample arrays
// yield peak_to_peak == 0. Throws std::invalid_argument when either configuration
// value is zero.
PipelineReport process_frames(const std::vector<Frame>& frames,
                              std::size_t worker_count,
                              std::size_t queue_capacity);

}  // namespace systems_course::week04

