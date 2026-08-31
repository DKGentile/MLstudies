#pragma once

#include "byte_stream.hpp"

#include <cstdint>

namespace systems_course::week04::net {

class TcpListener;

// Move-only ownership of one connected TCP socket. Platform handle types and
// Winsock process initialization remain in the supplied implementation file.
class TcpConnection final : public ByteStream {
 public:
  TcpConnection() noexcept = default;
  ~TcpConnection() override;

  TcpConnection(TcpConnection&& other) noexcept;
  TcpConnection& operator=(TcpConnection&& other) noexcept;

  TcpConnection(const TcpConnection&) = delete;
  TcpConnection& operator=(const TcpConnection&) = delete;

  std::size_t send_some(const std::byte* data,
                        std::size_t byte_count) override;
  std::size_t recv_some(std::byte* destination,
                        std::size_t capacity) override;
  void shutdown_write() override;

  bool valid() const noexcept;
  void close() noexcept;

 private:
  static constexpr std::uintptr_t invalid_handle = ~std::uintptr_t{0};

  explicit TcpConnection(std::uintptr_t handle) noexcept;

  std::uintptr_t handle_ = invalid_handle;

  friend class TcpListener;
  friend TcpConnection connect_loopback(std::uint16_t port);
};

// Move-only ownership of an IPv4 listener bound only to 127.0.0.1. Port zero
// requests an ephemeral port, which local_port() reports after binding.
class TcpListener {
 public:
  TcpListener() noexcept = default;
  ~TcpListener();

  TcpListener(TcpListener&& other) noexcept;
  TcpListener& operator=(TcpListener&& other) noexcept;

  TcpListener(const TcpListener&) = delete;
  TcpListener& operator=(const TcpListener&) = delete;

  static TcpListener bind_loopback(std::uint16_t port = 0, int backlog = 8);

  std::uint16_t local_port() const;
  TcpConnection accept();
  bool valid() const noexcept;
  void close() noexcept;

 private:
  static constexpr std::uintptr_t invalid_handle = ~std::uintptr_t{0};

  explicit TcpListener(std::uintptr_t handle) noexcept;

  std::uintptr_t handle_ = invalid_handle;
};

// Connects synchronously to an IPv4 listener on this host. Port zero is invalid.
TcpConnection connect_loopback(std::uint16_t port);

}  // namespace systems_course::week04::net
