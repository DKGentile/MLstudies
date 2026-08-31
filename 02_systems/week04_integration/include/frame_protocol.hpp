#pragma once

#include "byte_stream.hpp"
#include "frame_pipeline.hpp"

#include <cstddef>
#include <stdexcept>
#include <vector>

namespace systems_course::week04 {

inline constexpr std::size_t frame_prefix_bytes = 4;
inline constexpr std::size_t frame_fixed_body_bytes = 12;
inline constexpr std::size_t default_max_frame_body_bytes = 1024U * 1024U;

class ProtocolError : public std::runtime_error {
 public:
  using std::runtime_error::runtime_error;
};

// Wire format:
//   uint32 body byte count (big-endian)
//   uint64 sequence        (big-endian)
//   uint32 sample count    (big-endian)
//   int32  samples[]       (two's-complement bits, big-endian)
// The body length must equal 12 + 4 * sample_count.
std::vector<std::byte> encode_frame(const Frame& frame);

// Incrementally recovers frames from arbitrary stream chunks. One push may
// produce zero, one, or many frames. finish() accepts EOF only at an exact frame
// boundary and throws ProtocolError for a partial prefix or body.
class FrameDecoder {
 public:
  explicit FrameDecoder(
      std::size_t max_body_bytes = default_max_frame_body_bytes);

  std::vector<Frame> push(const std::byte* data, std::size_t byte_count);
  void finish() const;

  std::size_t buffered_bytes() const noexcept { return buffer_.size(); }

 private:
  std::size_t max_body_bytes_;
  std::vector<std::byte> buffer_;
};

// Completes one logical write despite short successful send_some() calls.
// Empty ranges succeed without touching the stream. Zero progress for a
// nonempty remainder throws std::runtime_error rather than spinning forever.
void write_all(net::ByteStream& stream, const std::byte* data,
               std::size_t byte_count);

inline void write_all(net::ByteStream& stream,
                      const std::vector<std::byte>& bytes) {
  write_all(stream, bytes.data(), bytes.size());
}

void send_frame(net::ByteStream& stream, const Frame& frame);

}  // namespace systems_course::week04
