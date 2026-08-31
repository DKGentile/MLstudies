#include "tcp_socket.hpp"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <system_error>
#include <utility>

#if defined(_WIN32)
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#include <winsock2.h>
#include <ws2tcpip.h>
#else
#include <cerrno>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#endif

namespace systems_course::week04::net {
namespace {

#if defined(_WIN32)

using NativeSocket = SOCKET;
constexpr NativeSocket invalid_native_socket = INVALID_SOCKET;

class WinsockRuntime {
 public:
  WinsockRuntime() {
    WSADATA data{};
    const int result = WSAStartup(MAKEWORD(2, 2), &data);
    if (result != 0) {
      throw std::system_error(result, std::system_category(), "WSAStartup");
    }
  }

  ~WinsockRuntime() { WSACleanup(); }

  WinsockRuntime(const WinsockRuntime&) = delete;
  WinsockRuntime& operator=(const WinsockRuntime&) = delete;
};

void ensure_socket_runtime() {
  static WinsockRuntime runtime;
  (void)runtime;
}

int last_socket_error() { return WSAGetLastError(); }

void close_native(NativeSocket socket) noexcept {
  if (socket != invalid_native_socket) {
    (void)closesocket(socket);
  }
}

#else

using NativeSocket = int;
constexpr NativeSocket invalid_native_socket = -1;

void ensure_socket_runtime() {}

int last_socket_error() { return errno; }

void close_native(NativeSocket socket) noexcept {
  if (socket != invalid_native_socket) {
    (void)::close(socket);
  }
}

#endif

[[noreturn]] void throw_socket_error(const char* operation) {
  throw std::system_error(last_socket_error(), std::system_category(), operation);
}

NativeSocket to_native(std::uintptr_t handle) noexcept {
  return static_cast<NativeSocket>(handle);
}

std::uintptr_t from_native(NativeSocket socket) noexcept {
  return static_cast<std::uintptr_t>(socket);
}

std::size_t bounded_io_count(std::size_t requested) noexcept {
  constexpr auto native_max = static_cast<std::size_t>(
      (std::numeric_limits<int>::max)());
  return (std::min)(requested, native_max);
}

}  // namespace

TcpConnection::TcpConnection(std::uintptr_t handle) noexcept : handle_(handle) {}

TcpConnection::~TcpConnection() { close(); }

TcpConnection::TcpConnection(TcpConnection&& other) noexcept
    : handle_(std::exchange(other.handle_, invalid_handle)) {}

TcpConnection& TcpConnection::operator=(TcpConnection&& other) noexcept {
  if (this != &other) {
    close();
    handle_ = std::exchange(other.handle_, invalid_handle);
  }
  return *this;
}

std::size_t TcpConnection::send_some(const std::byte* data,
                                     std::size_t byte_count) {
  if (!valid()) {
    throw std::logic_error("send_some called on a closed TCP connection");
  }
  if (byte_count == 0) {
    return 0;
  }
  if (data == nullptr) {
    throw std::invalid_argument("send_some data is null for a nonempty range");
  }

  const int requested = static_cast<int>(bounded_io_count(byte_count));
#if defined(_WIN32)
  const int result = ::send(to_native(handle_),
                            reinterpret_cast<const char*>(data), requested, 0);
  if (result == SOCKET_ERROR) {
    throw_socket_error("send");
  }
#else
  int flags = 0;
#if defined(MSG_NOSIGNAL)
  flags |= MSG_NOSIGNAL;
#endif
  int result = -1;
  do {
    result = static_cast<int>(
        ::send(to_native(handle_), data, static_cast<std::size_t>(requested),
               flags));
  } while (result < 0 && errno == EINTR);
  if (result < 0) {
    throw_socket_error("send");
  }
#endif
  return static_cast<std::size_t>(result);
}

std::size_t TcpConnection::recv_some(std::byte* destination,
                                     std::size_t capacity) {
  if (!valid()) {
    throw std::logic_error("recv_some called on a closed TCP connection");
  }
  if (capacity == 0) {
    throw std::invalid_argument("recv_some capacity must be positive");
  }
  if (destination == nullptr) {
    throw std::invalid_argument("recv_some destination is null");
  }

  const int requested = static_cast<int>(bounded_io_count(capacity));
#if defined(_WIN32)
  const int result = ::recv(to_native(handle_),
                            reinterpret_cast<char*>(destination), requested, 0);
  if (result == SOCKET_ERROR) {
    throw_socket_error("recv");
  }
#else
  int result = -1;
  do {
    result = static_cast<int>(
        ::recv(to_native(handle_), destination,
               static_cast<std::size_t>(requested), 0));
  } while (result < 0 && errno == EINTR);
  if (result < 0) {
    throw_socket_error("recv");
  }
#endif
  return static_cast<std::size_t>(result);
}

void TcpConnection::shutdown_write() {
  if (!valid()) {
    throw std::logic_error("shutdown_write called on a closed TCP connection");
  }
#if defined(_WIN32)
  if (::shutdown(to_native(handle_), SD_SEND) == SOCKET_ERROR) {
#else
  if (::shutdown(to_native(handle_), SHUT_WR) != 0) {
#endif
    throw_socket_error("shutdown write");
  }
}

bool TcpConnection::valid() const noexcept { return handle_ != invalid_handle; }

void TcpConnection::close() noexcept {
  if (valid()) {
    close_native(to_native(handle_));
    handle_ = invalid_handle;
  }
}

TcpListener::TcpListener(std::uintptr_t handle) noexcept : handle_(handle) {}

TcpListener::~TcpListener() { close(); }

TcpListener::TcpListener(TcpListener&& other) noexcept
    : handle_(std::exchange(other.handle_, invalid_handle)) {}

TcpListener& TcpListener::operator=(TcpListener&& other) noexcept {
  if (this != &other) {
    close();
    handle_ = std::exchange(other.handle_, invalid_handle);
  }
  return *this;
}

TcpListener TcpListener::bind_loopback(std::uint16_t port, int backlog) {
  if (backlog <= 0) {
    throw std::invalid_argument("TCP listen backlog must be positive");
  }
  ensure_socket_runtime();

  const NativeSocket socket = ::socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (socket == invalid_native_socket) {
    throw_socket_error("socket");
  }

  sockaddr_in address{};
  address.sin_family = AF_INET;
  address.sin_port = htons(port);
  address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  if (::bind(socket, reinterpret_cast<const sockaddr*>(&address),
             static_cast<int>(sizeof(address))) != 0) {
    const int error = last_socket_error();
    close_native(socket);
    throw std::system_error(error, std::system_category(), "bind loopback");
  }
  if (::listen(socket, backlog) != 0) {
    const int error = last_socket_error();
    close_native(socket);
    throw std::system_error(error, std::system_category(), "listen");
  }

  return TcpListener(from_native(socket));
}

std::uint16_t TcpListener::local_port() const {
  if (!valid()) {
    throw std::logic_error("local_port called on a closed TCP listener");
  }
  sockaddr_in address{};
#if defined(_WIN32)
  int address_size = static_cast<int>(sizeof(address));
#else
  socklen_t address_size = static_cast<socklen_t>(sizeof(address));
#endif
  if (::getsockname(to_native(handle_), reinterpret_cast<sockaddr*>(&address),
                    &address_size) != 0) {
    throw_socket_error("getsockname");
  }
  return ntohs(address.sin_port);
}

TcpConnection TcpListener::accept() {
  if (!valid()) {
    throw std::logic_error("accept called on a closed TCP listener");
  }

  NativeSocket connection = invalid_native_socket;
#if defined(_WIN32)
  connection = ::accept(to_native(handle_), nullptr, nullptr);
#else
  do {
    connection = ::accept(to_native(handle_), nullptr, nullptr);
  } while (connection == invalid_native_socket && errno == EINTR);
#endif
  if (connection == invalid_native_socket) {
    throw_socket_error("accept");
  }
  return TcpConnection(from_native(connection));
}

bool TcpListener::valid() const noexcept { return handle_ != invalid_handle; }

void TcpListener::close() noexcept {
  if (valid()) {
    close_native(to_native(handle_));
    handle_ = invalid_handle;
  }
}

TcpConnection connect_loopback(std::uint16_t port) {
  if (port == 0) {
    throw std::invalid_argument("TCP destination port must be nonzero");
  }
  ensure_socket_runtime();

  const NativeSocket socket = ::socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (socket == invalid_native_socket) {
    throw_socket_error("socket");
  }

  sockaddr_in address{};
  address.sin_family = AF_INET;
  address.sin_port = htons(port);
  address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

  if (::connect(socket, reinterpret_cast<const sockaddr*>(&address),
                static_cast<int>(sizeof(address))) != 0) {
    const int error = last_socket_error();
    close_native(socket);
    throw std::system_error(error, std::system_category(), "connect loopback");
  }
  return TcpConnection(from_native(socket));
}

}  // namespace systems_course::week04::net
