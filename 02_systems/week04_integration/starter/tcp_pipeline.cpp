#include "tcp_pipeline.hpp"

#include "bounded_queue.hpp"

#include <stdexcept>

namespace systems_course::week04 {

TcpPipelineReport receive_and_process_frames(net::ByteStream& stream,
                                             const TcpPipelineConfig& config) {
  if (config.worker_count == 0 || config.queue_capacity == 0 ||
      config.recv_chunk_bytes == 0) {
    throw std::invalid_argument(
        "worker count, queue capacity, and receive chunk must be positive");
  }
  if (config.max_frame_body_bytes < frame_fixed_body_bytes) {
    throw std::invalid_argument("maximum frame body is too small");
  }
  (void)stream;

  // LEARNER TODO: Start a fixed worker set around one bounded queue. The owner
  // thread must recv arbitrary chunks, pass them through FrameDecoder, and push
  // each completed frame immediately so a full queue stops further socket
  // reads. Preserve input position separately from Frame::sequence. Clean EOF
  // calls decoder.finish(), closes the queue, drains work, and joins. Every
  // exceptional path must also wake blocked users, join all owned threads, and
  // rethrow the first failure only after cleanup.
  throw std::logic_error(
      "LEARNER TODO: implement receive_and_process_frames");
}

}  // namespace systems_course::week04
