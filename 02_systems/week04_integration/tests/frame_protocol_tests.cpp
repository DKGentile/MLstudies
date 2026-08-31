#include "frame_protocol.hpp"
#include "test_support.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <initializer_list>
#include <limits>
#include <stdexcept>
#include <vector>

using systems_course::week04::Frame;
using systems_course::week04::FrameDecoder;
using systems_course::week04::ProtocolError;
using systems_course::week04::encode_frame;
using systems_course::week04::write_all;
using systems_course::week04::net::ByteStream;

namespace {

std::vector<std::byte> wire_bytes(
    std::initializer_list<unsigned int> values) {
  std::vector<std::byte> result;
  result.reserve(values.size());
  for (const auto value : values) {
    result.push_back(static_cast<std::byte>(value));
  }
  return result;
}

void append(std::vector<std::byte>& destination,
            const std::vector<std::byte>& source) {
  destination.insert(destination.end(), source.begin(), source.end());
}

class ShortWriteStream final : public ByteStream {
 public:
  explicit ShortWriteStream(std::size_t max_write) : max_write_(max_write) {}

  std::size_t send_some(const std::byte* data,
                        std::size_t byte_count) override {
    ++send_calls_;
    const std::size_t accepted = (std::min)(max_write_, byte_count);
    output_.insert(output_.end(), data, data + accepted);
    return accepted;
  }

  std::size_t recv_some(std::byte*, std::size_t) override {
    throw std::logic_error("receive is not used by this scripted stream");
  }

  void shutdown_write() override { shutdown_ = true; }

  const std::vector<std::byte>& output() const noexcept { return output_; }
  std::size_t send_calls() const noexcept { return send_calls_; }
  bool shutdown() const noexcept { return shutdown_; }

 private:
  std::size_t max_write_;
  std::size_t send_calls_ = 0;
  std::vector<std::byte> output_;
  bool shutdown_ = false;
};

}  // namespace

int main() {
  course_test::Suite suite;

  suite.run("encoder emits an exact length-prefixed big-endian frame", [] {
    const Frame frame{0x0102030405060708ULL, {0x01020304, -2}};
    const auto expected = wire_bytes({
        0x00, 0x00, 0x00, 0x14,              // 20-byte body
        0x01, 0x02, 0x03, 0x04,              // sequence
        0x05, 0x06, 0x07, 0x08,
        0x00, 0x00, 0x00, 0x02,              // two samples
        0x01, 0x02, 0x03, 0x04,              // +0x01020304
        0xFF, 0xFF, 0xFF, 0xFE,              // -2 bit pattern
    });
    COURSE_CHECK(encode_frame(frame) == expected);
  });

  suite.run("decoder accepts every single split point", [] {
    const Frame expected{42, {-9, 0, 17}};
    const auto encoded = encode_frame(expected);
    for (std::size_t split = 0; split <= encoded.size(); ++split) {
      FrameDecoder decoder;
      std::vector<Frame> decoded;
      const auto first = decoder.push(encoded.data(), split);
      decoded.insert(decoded.end(), first.begin(), first.end());
      const auto second = decoder.push(encoded.data() + split,
                                       encoded.size() - split);
      decoded.insert(decoded.end(), second.begin(), second.end());
      decoder.finish();
      COURSE_CHECK(decoded == std::vector<Frame>{expected});
    }
  });

  suite.run("one input chunk may contain several application messages", [] {
    const Frame first{7, {1}};
    const Frame second{8, {2, 3}};
    auto coalesced = encode_frame(first);
    append(coalesced, encode_frame(second));

    FrameDecoder decoder;
    const auto decoded = decoder.push(coalesced.data(), coalesced.size());
    decoder.finish();
    COURSE_CHECK(decoded == std::vector<Frame>({first, second}));
  });

  suite.run("empty payload and signed sample extrema round-trip", [] {
    const Frame empty{0, {}};
    const Frame extrema{
        (std::numeric_limits<std::uint64_t>::max)(),
        {(std::numeric_limits<std::int32_t>::min)(),
         (std::numeric_limits<std::int32_t>::max)()}};
    auto bytes = encode_frame(empty);
    append(bytes, encode_frame(extrema));

    FrameDecoder decoder;
    const auto decoded = decoder.push(bytes.data(), bytes.size());
    decoder.finish();
    COURSE_CHECK(decoded == std::vector<Frame>({empty, extrema}));
  });

  suite.run("decoder rejects invalid lengths, counts, and truncated frames", [] {
    bool rejected_undersized = false;
    bool rejected_oversized = false;
    bool rejected_count_mismatch = false;
    bool rejected_truncated = false;

    try {
      FrameDecoder decoder;
      const auto bytes = wire_bytes({0x00, 0x00, 0x00, 0x0B});
      (void)decoder.push(bytes.data(), bytes.size());
    } catch (const ProtocolError&) {
      rejected_undersized = true;
    }

    try {
      FrameDecoder decoder(16);
      const auto bytes = wire_bytes({0x00, 0x00, 0x00, 0x20});
      (void)decoder.push(bytes.data(), bytes.size());
    } catch (const ProtocolError&) {
      rejected_oversized = true;
    }

    try {
      FrameDecoder decoder;
      const auto bytes = wire_bytes({
          0x00, 0x00, 0x00, 0x10,  // valid 16-byte body length
          0x00, 0x00, 0x00, 0x00,  // sequence
          0x00, 0x00, 0x00, 0x01,
          0x00, 0x00, 0x00, 0x02,  // claims two samples
          0x00, 0x00, 0x00, 0x2A,  // but body holds only one
      });
      (void)decoder.push(bytes.data(), bytes.size());
    } catch (const ProtocolError&) {
      rejected_count_mismatch = true;
    }

    try {
      FrameDecoder decoder;
      const auto bytes = wire_bytes({0x00, 0x00, 0x00});
      (void)decoder.push(bytes.data(), bytes.size());
      decoder.finish();
    } catch (const ProtocolError&) {
      rejected_truncated = true;
    }

    COURSE_CHECK(rejected_undersized);
    COURSE_CHECK(rejected_oversized);
    COURSE_CHECK(rejected_count_mismatch);
    COURSE_CHECK(rejected_truncated);
  });

  suite.run("write_all advances by short successful writes", [] {
    const auto input = wire_bytes(
        {0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19});
    ShortWriteStream stream(3);
    write_all(stream, input);
    COURSE_CHECK(stream.output() == input);
    COURSE_CHECK(stream.send_calls() == 4U);
    COURSE_CHECK(!stream.shutdown());
  });

  suite.run("zero write progress is an error instead of an infinite loop", [] {
    ShortWriteStream stream(0);
    const auto input = wire_bytes({0xAA});
    bool rejected_zero_progress = false;
    try {
      write_all(stream, input);
    } catch (const std::runtime_error&) {
      rejected_zero_progress = true;
    }
    COURSE_CHECK(rejected_zero_progress);
    COURSE_CHECK(stream.send_calls() == 1U);
  });

  return suite.finish();
}
