#include "tcp_socket.hpp"
#include "test_support.hpp"

#include <cstddef>
#include <exception>
#include <future>
#include <stdexcept>
#include <thread>
#include <utility>

using systems_course::week04::net::TcpListener;
using systems_course::week04::net::connect_loopback;

int main() {
  course_test::Suite suite;

  suite.run("supplied TCP owner exchanges bytes and reports FIN on loopback", [] {
    auto listener = TcpListener::bind_loopback(0);
    const auto port = listener.local_port();
    COURSE_CHECK(port != 0);

    std::promise<void> server_promise;
    auto server_result = server_promise.get_future();
    std::thread server([listener = std::move(listener),
                        promise = std::move(server_promise)]() mutable {
      try {
        auto connection = listener.accept();
        std::byte request{};
        const auto received = connection.recv_some(&request, 1);
        if (received != 1 || request != std::byte{0x5A}) {
          throw std::runtime_error("server received the wrong byte");
        }
        const std::byte reply{0xA5};
        if (connection.send_some(&reply, 1) != 1) {
          throw std::runtime_error("server reply did not make progress");
        }
        std::byte after_fin{};
        if (connection.recv_some(&after_fin, 1) != 0) {
          throw std::runtime_error("server expected EOF after client FIN");
        }
        connection.shutdown_write();
        promise.set_value();
      } catch (...) {
        promise.set_exception(std::current_exception());
      }
    });

    std::exception_ptr client_error;
    try {
      auto client = connect_loopback(port);
      const std::byte request{0x5A};
      COURSE_CHECK(client.send_some(&request, 1) == 1U);
      client.shutdown_write();
      std::byte reply{};
      COURSE_CHECK(client.recv_some(&reply, 1) == 1U);
      COURSE_CHECK(reply == std::byte{0xA5});
      COURSE_CHECK(client.recv_some(&reply, 1) == 0U);
    } catch (...) {
      client_error = std::current_exception();
    }

    server.join();
    server_result.get();
    if (client_error) {
      std::rethrow_exception(client_error);
    }
  });

  suite.run("socket owners are move-only and moved-from owners are empty", [] {
    auto listener = TcpListener::bind_loopback(0);
    const auto port = listener.local_port();
    TcpListener moved = std::move(listener);
    COURSE_CHECK(!listener.valid());
    COURSE_CHECK(moved.valid());
    COURSE_CHECK(moved.local_port() == port);
    moved.close();
    moved.close();
    COURSE_CHECK(!moved.valid());
  });

  suite.run("invalid listener and destination bounds are rejected", [] {
    bool rejected_backlog = false;
    bool rejected_port = false;
    try {
      (void)TcpListener::bind_loopback(0, 0);
    } catch (const std::invalid_argument&) {
      rejected_backlog = true;
    }
    try {
      (void)connect_loopback(0);
    } catch (const std::invalid_argument&) {
      rejected_port = true;
    }
    COURSE_CHECK(rejected_backlog);
    COURSE_CHECK(rejected_port);
  });

  return suite.finish();
}
