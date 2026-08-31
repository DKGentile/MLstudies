#include "frame_protocol.hpp"
#include "tcp_socket.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <exception>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

using systems_course::week04::Frame;
using systems_course::week04::encode_frame;
using systems_course::week04::write_all;
using systems_course::week04::net::ByteStream;
using systems_course::week04::net::TcpConnection;
using systems_course::week04::net::connect_loopback;

namespace {

std::size_t parse_size(const char* text, const char* label) {
  if (text[0] == '-') {
    throw std::invalid_argument(std::string(label) + " must be nonnegative");
  }
  std::size_t consumed = 0;
  const auto parsed = std::stoull(text, &consumed);
  if (text[consumed] != '\0' ||
      parsed > (std::numeric_limits<std::size_t>::max)()) {
    throw std::invalid_argument(std::string("invalid ") + label);
  }
  return static_cast<std::size_t>(parsed);
}

std::uint16_t parse_port(const char* text) {
  const auto parsed = parse_size(text, "port");
  if (parsed == 0 || parsed > 65535) {
    throw std::invalid_argument("port must be in [1, 65535]");
  }
  return static_cast<std::uint16_t>(parsed);
}

class ExperimentStream final : public ByteStream {
 public:
  ExperimentStream(TcpConnection& connection, std::size_t max_send_chunk,
                   std::size_t disconnect_after)
      : connection_(connection),
        max_send_chunk_(max_send_chunk),
        disconnect_after_(disconnect_after) {}

  std::size_t send_some(const std::byte* data,
                        std::size_t byte_count) override {
    if (disconnect_after_ != 0 && sent_bytes_ >= disconnect_after_) {
      disconnected_ = true;
      connection_.close();
      throw std::runtime_error("intentional producer disconnect");
    }

    std::size_t offered = byte_count;
    if (max_send_chunk_ != 0) {
      offered = (std::min)(offered, max_send_chunk_);
    }
    if (disconnect_after_ != 0) {
      offered = (std::min)(offered, disconnect_after_ - sent_bytes_);
    }
    const auto sent = connection_.send_some(data, offered);
    sent_bytes_ += sent;
    return sent;
  }

  std::size_t recv_some(std::byte* destination,
                        std::size_t capacity) override {
    return connection_.recv_some(destination, capacity);
  }

  void shutdown_write() override {
    if (disconnect_after_ != 0 && sent_bytes_ >= disconnect_after_) {
      disconnected_ = true;
      connection_.close();
      throw std::runtime_error("intentional producer disconnect");
    }
    connection_.shutdown_write();
  }

  std::size_t sent_bytes() const noexcept { return sent_bytes_; }
  bool disconnected() const noexcept { return disconnected_; }

 private:
  TcpConnection& connection_;
  std::size_t max_send_chunk_;
  std::size_t disconnect_after_;
  std::size_t sent_bytes_ = 0;
  bool disconnected_ = false;
};

Frame make_frame(std::size_t frame_index, std::size_t sample_count) {
  Frame frame;
  frame.sequence = frame_index;
  frame.samples.reserve(sample_count);
  for (std::size_t sample = 0; sample < sample_count; ++sample) {
    const auto value = static_cast<std::int32_t>(
        (frame_index + sample) % 2001U) - 1000;
    frame.samples.push_back(value);
  }
  return frame;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc < 3 || argc > 6) {
    std::cerr
        << "usage: systems_fake_sensor PORT FRAME_COUNT [SAMPLES_PER_FRAME] "
           "[MAX_SEND_CHUNK] [DISCONNECT_AFTER_BYTES]\n";
    return 64;
  }

  try {
    const auto port = parse_port(argv[1]);
    const auto frame_count = parse_size(argv[2], "frame count");
    const auto samples_per_frame =
        argc >= 4 ? parse_size(argv[3], "samples per frame") : 64U;
    const auto max_send_chunk =
        argc >= 5 ? parse_size(argv[4], "maximum send chunk") : 0U;
    const auto disconnect_after =
        argc >= 6 ? parse_size(argv[5], "disconnect byte count") : 0U;
    if (samples_per_frame > 1000000U) {
      throw std::invalid_argument(
          "samples per frame is capped at 1,000,000 for this probe");
    }

    auto connection = connect_loopback(port);
    ExperimentStream stream(connection, max_send_chunk, disconnect_after);
    try {
      for (std::size_t index = 0; index < frame_count; ++index) {
        const auto encoded = encode_frame(make_frame(index, samples_per_frame));
        write_all(stream, encoded);
      }
      stream.shutdown_write();
    } catch (...) {
      if (stream.disconnected()) {
        std::cerr << "intentional_disconnect_after=" << stream.sent_bytes()
                  << "\n";
        return 2;
      }
      throw;
    }

    std::cout << "frames_sent=" << frame_count << '\n'
              << "bytes_sent=" << stream.sent_bytes() << '\n'
              << "max_send_chunk=" << max_send_chunk << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "fake sensor failed: " << error.what() << '\n';
    return 1;
  }
}
