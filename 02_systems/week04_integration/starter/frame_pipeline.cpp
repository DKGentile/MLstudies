#include "frame_pipeline.hpp"

#include "bounded_queue.hpp"

#include <stdexcept>

namespace systems_course::week04 {

PipelineReport process_frames(const std::vector<Frame>& frames,
                              std::size_t worker_count,
                              std::size_t queue_capacity) {
  (void)frames;
  (void)worker_count;
  (void)queue_capacity;

  // LEARNER TODO: Use systems_course::week03::BoundedQueue as the bounded handoff.
  // Preserve input positions separately from Frame::sequence so duplicate
  // sequence values remain well-defined. Own and join every worker on all paths.
  throw std::logic_error("LEARNER TODO: implement process_frames");
}

}  // namespace systems_course::week04
