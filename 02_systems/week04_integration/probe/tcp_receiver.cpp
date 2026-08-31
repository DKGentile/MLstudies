#include "tcp_pipeline.hpp"
#include "tcp_socket.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <exception>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

using systems_course::week04::TcpPipelineConfig;
using systems_course::week04::receive_and_process_frames;
using systems_course::week04::net::TcpListener;

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
  if (parsed > 65535) {
    throw std::invalid_argument("port must be in [0, 65535]");
  }
  return static_cast<std::uint16_t>(parsed);
}

}  // namespace

int main(int argc, char** argv) {
  if (argc < 4 || argc > 6) {
    std::cerr << "usage: systems_tcp_receiver PORT WORKERS CAPACITY "
                 "[RECV_CHUNK] [MAX_FRAME_BODY]\n";
    return 64;
  }

  try {
    const auto port = parse_port(argv[1]);
    TcpPipelineConfig config;
    config.worker_count = parse_size(argv[2], "worker count");
    config.queue_capacity = parse_size(argv[3], "queue capacity");
    if (argc >= 5) {
      config.recv_chunk_bytes = parse_size(argv[4], "receive chunk");
    }
    if (argc >= 6) {
      config.max_frame_body_bytes = parse_size(argv[5], "maximum frame body");
    }

    auto listener = TcpListener::bind_loopback(port);
    std::cout << "listening_address=127.0.0.1\n"
              << "listening_port=" << listener.local_port() << '\n';
    std::cout.flush();

    auto connection = listener.accept();
    const auto report = receive_and_process_frames(connection, config);
    std::cout << "received_frames=" << report.received_frames << '\n'
              << "received_bytes=" << report.received_bytes << '\n'
              << "recv_calls=" << report.recv_calls << '\n'
              << "clean_eof=" << (report.clean_eof ? "true" : "false")
              << '\n'
              << "processed_results=" << report.pipeline.results.size()
              << '\n';

    const auto preview_count =
        (std::min)(report.pipeline.results.size(), std::size_t{10});
    for (std::size_t index = 0; index < preview_count; ++index) {
      const auto& result = report.pipeline.results[index];
      std::cout << "result[" << index << "].sequence=" << result.sequence
                << " peak_to_peak=" << result.peak_to_peak << '\n';
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "TCP receiver failed: " << error.what() << '\n';
    return 1;
  }
}
