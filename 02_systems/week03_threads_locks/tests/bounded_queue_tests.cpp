#include "bounded_queue.hpp"
#include "test_support.hpp"

#include <chrono>
#include <exception>
#include <future>
#include <optional>
#include <stdexcept>
#include <thread>

using systems_course::week03::BoundedQueue;
using namespace std::chrono_literals;

int main() {
  course_test::Suite suite;
  bool basic_operations_ready = false;
  bool close_operations_ready = false;

  suite.run("capacity is validated and queue is FIFO", [&] {
    bool rejected_zero = false;
    try {
      BoundedQueue<int> invalid(0);
    } catch (const std::invalid_argument&) {
      rejected_zero = true;
    }
    COURSE_CHECK(rejected_zero);

    BoundedQueue<int> queue(2);
    COURSE_CHECK(queue.push(10));
    COURSE_CHECK(queue.push(20));
    COURSE_CHECK(queue.pop() == std::optional<int>{10});
    COURSE_CHECK(queue.pop() == std::optional<int>{20});
    basic_operations_ready = true;
  });

  suite.run("close rejects producers, drains items, then signals end", [&] {
    BoundedQueue<int> queue(2);
    COURSE_CHECK(queue.push(5));
    queue.close();
    queue.close();
    COURSE_CHECK(queue.closed());
    COURSE_CHECK(!queue.push(6));
    COURSE_CHECK(queue.pop() == std::optional<int>{5});
    COURSE_CHECK(!queue.pop().has_value());
    close_operations_ready = true;
  });

  suite.run("empty pop blocks until a producer makes progress", [&] {
    if (!basic_operations_ready) {
      throw std::runtime_error("finish basic FIFO operations before blocking test");
    }

    BoundedQueue<int> queue(1);
    std::promise<std::optional<int>> promise;
    auto result = promise.get_future();
    std::thread consumer([&] {
      try {
        promise.set_value(queue.pop());
      } catch (...) {
        promise.set_exception(std::current_exception());
      }
    });

    const auto before_push = result.wait_for(50ms);
    bool push_accepted = false;
    std::exception_ptr push_error;
    try {
      push_accepted = queue.push(91);
    } catch (...) {
      push_error = std::current_exception();
      try {
        queue.close();
      } catch (...) {
        // The outer CTest timeout still diagnoses a partial implementation that
        // cannot wake this waiter. Preserve the original push failure.
      }
    }
    const auto after_push = result.wait_for(1s);
    if (after_push != std::future_status::ready) {
      queue.close();
    }
    consumer.join();

    if (push_error) {
      std::rethrow_exception(push_error);
    }
    COURSE_CHECK(before_push == std::future_status::timeout);
    COURSE_CHECK(after_push == std::future_status::ready);
    COURSE_CHECK(push_accepted);
    COURSE_CHECK(result.get() == std::optional<int>{91});
  });

  suite.run("close wakes a consumer waiting on an empty queue", [&] {
    if (!basic_operations_ready || !close_operations_ready) {
      throw std::runtime_error("finish FIFO and close operations before wake test");
    }

    BoundedQueue<int> queue(1);
    std::promise<std::optional<int>> promise;
    auto result = promise.get_future();
    std::thread consumer([&] {
      try {
        promise.set_value(queue.pop());
      } catch (...) {
        promise.set_exception(std::current_exception());
      }
    });

    const auto before_close = result.wait_for(50ms);
    queue.close();
    const auto after_close = result.wait_for(1s);
    consumer.join();

    COURSE_CHECK(before_close == std::future_status::timeout);
    COURSE_CHECK(after_close == std::future_status::ready);
    COURSE_CHECK(!result.get().has_value());
  });

  suite.run("full push blocks until a consumer makes space", [&] {
    if (!basic_operations_ready || !close_operations_ready) {
      throw std::runtime_error("finish FIFO and close operations before blocking test");
    }

    BoundedQueue<int> queue(1);
    COURSE_CHECK(queue.push(1));
    std::promise<bool> promise;
    auto result = promise.get_future();
    std::thread producer([&] {
      try {
        promise.set_value(queue.push(2));
      } catch (...) {
        promise.set_exception(std::current_exception());
      }
    });

    const auto before_pop = result.wait_for(50ms);
    std::optional<int> first_value;
    std::exception_ptr pop_error;
    try {
      first_value = queue.pop();
    } catch (...) {
      pop_error = std::current_exception();
      try {
        queue.close();
      } catch (...) {
        // Preserve the original failure; CTest bounds any broken wake path.
      }
    }
    const auto after_pop = result.wait_for(1s);
    if (after_pop != std::future_status::ready) {
      queue.close();
    }
    producer.join();

    if (pop_error) {
      std::rethrow_exception(pop_error);
    }
    COURSE_CHECK(before_pop == std::future_status::timeout);
    COURSE_CHECK(after_pop == std::future_status::ready);
    COURSE_CHECK(first_value == std::optional<int>{1});
    COURSE_CHECK(result.get());
    COURSE_CHECK(queue.pop() == std::optional<int>{2});
  });

  return suite.finish();
}
