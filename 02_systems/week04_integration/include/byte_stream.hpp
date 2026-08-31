#pragma once

#include <cstddef>

namespace systems_course::week04::net {

// A narrow seam around stream I/O. TcpConnection is the real implementation;
// tests provide scripted implementations so short reads and writes are
// deterministic instead of depending on kernel buffer timing.
class ByteStream {
 public:
  virtual ~ByteStream() = default;

  ByteStream() = default;
  ByteStream(const ByteStream&) = delete;
  ByteStream& operator=(const ByteStream&) = delete;

  // Attempts to send at most byte_count bytes and returns the number accepted.
  // A positive request may complete only partially. Throws std::system_error
  // for transport errors.
  virtual std::size_t send_some(const std::byte* data,
                                std::size_t byte_count) = 0;

  // Receives at most capacity bytes. A positive return is data; zero means the
  // peer reached EOF. Callers must provide nonzero capacity.
  virtual std::size_t recv_some(std::byte* destination,
                                std::size_t capacity) = 0;

  // Sends TCP FIN after pending bytes while leaving the read side available.
  virtual void shutdown_write() = 0;
};

}  // namespace systems_course::week04::net
