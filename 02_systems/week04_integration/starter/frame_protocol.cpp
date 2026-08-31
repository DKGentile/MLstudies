#include "frame_protocol.hpp"

#include <stdexcept>

namespace systems_course::week04 {

std::vector<std::byte> encode_frame(const Frame& frame) {
  (void)frame;
  // LEARNER TODO: Validate representable body/sample counts, then append the
  // prefix and fields explicitly in network (big-endian) byte order. Do not
  // serialize the in-memory struct representation or use pointer punning.
  throw std::logic_error("LEARNER TODO: implement encode_frame");
}

FrameDecoder::FrameDecoder(std::size_t max_body_bytes)
    : max_body_bytes_(max_body_bytes) {
  if (max_body_bytes < frame_fixed_body_bytes) {
    throw std::invalid_argument(
        "maximum frame body must hold sequence and sample count");
  }
}

std::vector<Frame> FrameDecoder::push(const std::byte* data,
                                      std::size_t byte_count) {
  if (data == nullptr && byte_count != 0) {
    throw std::invalid_argument("decoder data is null for a nonempty chunk");
  }
  (void)data;
  (void)byte_count;

  // LEARNER TODO: Append this arbitrary chunk, then repeatedly decode every
  // complete frame currently buffered. A prefix may be split across calls, and
  // one call may contain several frames. Reject a body larger than
  // max_body_bytes_ before allocating or waiting for it. Validate the sample
  // count/body-size relationship with overflow-safe arithmetic.
  throw std::logic_error("LEARNER TODO: implement FrameDecoder::push");
}

void FrameDecoder::finish() const {
  // LEARNER TODO: EOF is clean only when no partial prefix/body remains.
  throw std::logic_error("LEARNER TODO: implement FrameDecoder::finish");
}

void write_all(net::ByteStream& stream, const std::byte* data,
               std::size_t byte_count) {
  if (data == nullptr && byte_count != 0) {
    throw std::invalid_argument("write_all data is null for a nonempty range");
  }
  if (byte_count == 0) {
    return;
  }
  (void)stream;
  (void)data;
  (void)byte_count;

  // LEARNER TODO: Loop until every byte is accepted. Advance by the returned
  // count, never by the requested count. Treat zero progress on a nonempty
  // remainder as an error so the caller cannot spin forever.
  throw std::logic_error("LEARNER TODO: implement write_all");
}

void send_frame(net::ByteStream& stream, const Frame& frame) {
  const auto bytes = encode_frame(frame);
  write_all(stream, bytes);
}

}  // namespace systems_course::week04
