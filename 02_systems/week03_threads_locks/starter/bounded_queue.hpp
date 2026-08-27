#pragma once

#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>
#include <stdexcept>
#include <utility>

namespace systems_course::week03 {

template <typename T>
class BoundedQueue {
 public:
  explicit BoundedQueue(std::size_t capacity) : capacity_(capacity) {
    if (capacity == 0) {
      throw std::invalid_argument("BoundedQueue capacity must be positive");
    }
  }

  BoundedQueue(const BoundedQueue&) = delete;
  BoundedQueue& operator=(const BoundedQueue&) = delete;

  // The owner must close the queue and join all users before destruction.

  // Blocks while full. Returns false instead of inserting when the queue closes.
  bool push(T item) {
    (void)item;
    throw std::logic_error("TODO: implement BoundedQueue::push");
  }

  // Blocks while empty. After close, drains queued items, then returns nullopt.
  std::optional<T> pop() {
    throw std::logic_error("TODO: implement BoundedQueue::pop");
  }

  // Idempotently closes the queue and unblocks every waiter.
  void close() {
    throw std::logic_error("TODO: implement BoundedQueue::close");
  }

  bool closed() const {
    throw std::logic_error("TODO: implement BoundedQueue::closed");
  }

 private:
  const std::size_t capacity_;
  mutable std::mutex mutex_;
  std::condition_variable not_empty_;
  std::condition_variable not_full_;
  std::deque<T> items_;
  bool closed_ = false;
};

}  // namespace systems_course::week03
