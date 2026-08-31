#pragma once

#include "byte_stream.hpp"
#include "frame_pipeline.hpp"
#include "frame_protocol.hpp"

#include <cstddef>

namespace systems_course::week04 {

struct TcpPipelineConfig {
  std::size_t worker_count = 1;
  std::size_t queue_capacity = 1;
  std::size_t recv_chunk_bytes = 4096;
  std::size_t max_frame_body_bytes = default_max_frame_body_bytes;
};

struct TcpPipelineReport {
  PipelineReport pipeline;
  // Counts complete application frames and raw wire bytes received.
  std::size_t received_frames = 0;
  std::size_t received_bytes = 0;
  // Includes the final recv_some call that returns zero for clean EOF.
  std::size_t recv_calls = 0;
  bool clean_eof = false;
};

// Reads frames incrementally from an already-connected stream and submits each
// complete frame directly to a bounded worker queue. It must not first collect
// the entire connection into an unbounded vector. On clean EOF, close and drain
// the queue, join all workers, and return ordered results. On protocol, I/O, or
// worker failure, wake blocked users, join every owned thread, then rethrow.
TcpPipelineReport receive_and_process_frames(net::ByteStream& stream,
                                             const TcpPipelineConfig& config);

}  // namespace systems_course::week04
