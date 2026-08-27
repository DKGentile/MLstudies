#pragma once

#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>

namespace course_test {

class Suite {
 public:
  template <typename Function>
  void run(std::string name, Function&& function) {
    try {
      function();
      ++passed_;
      std::cout << "[PASS] " << name << '\n';
    } catch (const std::exception& error) {
      ++failed_;
      std::cerr << "[FAIL] " << name << ": " << error.what() << '\n';
    } catch (...) {
      ++failed_;
      std::cerr << "[FAIL] " << name << ": unknown exception\n";
    }
  }

  int finish() const {
    std::cout << "\n" << passed_ << " passed, " << failed_ << " failed\n";
    return failed_ == 0 ? 0 : 1;
  }

 private:
  int passed_ = 0;
  int failed_ = 0;
};

inline void check(bool condition, const char* expression, const char* file,
                  int line) {
  if (!condition) {
    throw std::runtime_error(std::string(file) + ":" +
                             std::to_string(line) + " check failed: " +
                             expression);
  }
}

}  // namespace course_test

#define COURSE_CHECK(expression) \
  ::course_test::check(static_cast<bool>(expression), #expression, __FILE__, \
                       __LINE__)
