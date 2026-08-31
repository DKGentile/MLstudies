#include "frame_protocol.hpp"
#include "tcp_pipeline.hpp"
#include "tcp_socket.hpp"
#include "test_support.hpp"

#include <algorithm>
#include <cstddef>
#include <exception>
#include <future>
#include <stdexcept>
#include <thread>
#include <utility>
#include <vector>

using systems_course::week04::Frame;
using systems_course::week04::FrameResult;
using systems_course::week04::ProtocolError;
using systems_course::week04::TcpPipelineConfig;
using systems_course::week04::TcpPipelineReport;
using systems_course::week04::encode_frame;
using systems_course::week04::receive_and_process_frames;
using systems_course::week04::send_frame;
using systems_course::week04::net::ByteStream;
using systems_course::week04::net::TcpConnection;
using systems_course::week04::net::TcpListener;
using systems_course::week04::net::connect_loopback;

namespace {

class ScriptedReadStream final : public ByteStream {
 public:
  ScriptedReadStream(std::vector<std::byte> input, std::size_t max_read)
      : input_(std::move(input)), max_read_(max_read) {}

  std::size_t send_some(const std::byte*, std::size_t) override {
    throw std::logic_error("send is not used by this scripted stream");
  }

  std::size_t recv_some(std::byte* destination,
                        std::size_t capacity) override {
    ++recv_calls_;
    if (offset_ == input_.size()) {
      return 0;
    }
    const auto count =
        (std::min)({max_read_, capacity, input_.size() - offset_});
    std::copy_n(input_.data() + offset_, count, destination);
    offset_ += count;
    return count;
  }

  void shutdown_write() override {}

  std::size_t recv_calls() const noexcept { return recv_calls_; }

 private:
  std::vector<std::byte> input_;
  std::size_t max_read_;
  std::size_t offset_ = 0;
  std::size_t recv_calls_ = 0;
};

class CappedStream final : public ByteStream {
 public:
  CappedStream(TcpConnection& connection, std::size_t max_send)
      : connection_(connection), max_send_(max_send) {}

  std::size_t send_some(const std::byte* data,
                        std::size_t byte_count) override {
    return connection_.send_some(data, (std::min)(max_send_, byte_count));
  }

  std::size_t recv_some(std::byte* destination,
                        std::size_t capacity) override {
    return connection_.recv_some(destination, capacity);
  }

  void shutdown_write() override { connection_.shutdown_write(); }

 private:
  TcpConnection& connection_;
  std::size_t max_send_;
};

std::vector<std::byte> join_encoded(const std::vector<Frame>& frames) {
  std::vector<std::byte> bytes;
  for (const auto& frame : frames) {
    const auto encoded = encode_frame(frame);
    bytes.insert(bytes.end(), encoded.begin(), encoded.end());
  }
  return bytes;
}

TcpPipelineConfig small_config() {
  TcpPipelineConfig config;
  config.worker_count = 2;
  config.queue_capacity = 1;
  config.recv_chunk_bytes = 5;
  return config;
}

}  // namespace

int main() {
  course_test::Suite suite;

  suite.run("scripted one-byte reads still recover complete ordered frames", [] {
    const std::vector<Frame> frames{{10, {3, -2, 8, 1}},
                                    {4, {100}},
                                    {10, {}}};
    ScriptedReadStream stream(join_encoded(frames), 1);
    const auto report = receive_and_process_frames(stream, small_config());
    const std::vector<FrameResult> expected{{10, 10}, {4, 0}, {10, 0}};

    COURSE_CHECK(report.pipeline.worker_count == 2U);
    COURSE_CHECK(report.pipeline.queue_capacity == 1U);
    COURSE_CHECK(report.pipeline.results == expected);
    COURSE_CHECK(report.received_frames == frames.size());
    COURSE_CHECK(report.received_bytes > frames.size());
    COURSE_CHECK(report.recv_calls == stream.recv_calls());
    COURSE_CHECK(report.recv_calls > report.received_frames);
    COURSE_CHECK(report.clean_eof);
  });

  suite.run("real loopback fragments writes and drains after half-close", [] {
    auto listener = TcpListener::bind_loopback(0);
    const auto port = listener.local_port();
    const std::vector<Frame> frames{{3, {-1, 9}},
                                    {3, {}},
                                    {99, {-8, -4, -20}}};
    const auto expected_bytes = join_encoded(frames).size();

    std::promise<TcpPipelineReport> promise;
    auto future = promise.get_future();
    std::thread server([listener = std::move(listener),
                        promise = std::move(promise)]() mutable {
      try {
        auto connection = listener.accept();
        promise.set_value(receive_and_process_frames(connection, small_config()));
      } catch (...) {
        promise.set_exception(std::current_exception());
      }
    });

    std::exception_ptr client_error;
    try {
      auto connection = connect_loopback(port);
      CappedStream fragmented(connection, 3);
      for (const auto& frame : frames) {
        send_frame(fragmented, frame);
      }
      fragmented.shutdown_write();
    } catch (...) {
      client_error = std::current_exception();
    }

    server.join();
    const auto report = future.get();
    if (client_error) {
      std::rethrow_exception(client_error);
    }

    const std::vector<FrameResult> expected{{3, 10}, {3, 0}, {99, 16}};
    COURSE_CHECK(report.pipeline.results == expected);
    COURSE_CHECK(report.received_frames == frames.size());
    COURSE_CHECK(report.received_bytes == expected_bytes);
    COURSE_CHECK(report.clean_eof);
  });

  suite.run("disconnect in the middle of a frame is not clean EOF", [] {
    auto listener = TcpListener::bind_loopback(0);
    const auto port = listener.local_port();

    std::promise<bool> promise;
    auto future = promise.get_future();
    std::thread server([listener = std::move(listener),
                        promise = std::move(promise)]() mutable {
      try {
        auto connection = listener.accept();
        (void)receive_and_process_frames(connection, small_config());
        promise.set_value(false);
      } catch (const ProtocolError&) {
        promise.set_value(true);
      } catch (...) {
        promise.set_exception(std::current_exception());
      }
    });

    std::exception_ptr client_error;
    try {
      auto client = connect_loopback(port);
      // Prefix says a 12-byte body follows, but only one body byte is sent.
      const std::vector<std::byte> truncated{
          std::byte{0x00}, std::byte{0x00}, std::byte{0x00},
          std::byte{0x0C}, std::byte{0xAA}};
      for (const auto byte : truncated) {
        COURSE_CHECK(client.send_some(&byte, 1) == 1U);
      }
      client.close();
    } catch (...) {
      client_error = std::current_exception();
    }

    server.join();
    COURSE_CHECK(future.get());
    if (client_error) {
      std::rethrow_exception(client_error);
    }
  });

  suite.run("invalid pipeline bounds fail before starting threads", [] {
    ScriptedReadStream empty({}, 1);
    auto config = small_config();
    config.queue_capacity = 0;
    bool rejected = false;
    try {
      (void)receive_and_process_frames(empty, config);
    } catch (const std::invalid_argument&) {
      rejected = true;
    }
    COURSE_CHECK(rejected);
    COURSE_CHECK(empty.recv_calls() == 0U);
  });

  return suite.finish();
}
