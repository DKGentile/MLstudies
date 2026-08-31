#include <array>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

int selected_channel(std::size_t index) {
  const std::array<int, 4> channels{12, 24, 48, 96};
  return channels[index];
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const std::size_t index =
        argc == 2 ? static_cast<std::size_t>(std::stoull(argv[1])) : 4U;

    // INTENTIONAL BUG CLINIC: the default invocation must first be reproduced
    // with a debugger or sanitizer.
    // LEARNER TODO: repair the boundary contract, rerun the same diagnostic,
    // and explain why every possible index now has defined behavior.
    std::cout << "selected value: " << selected_channel(index) << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "bounds clinic input error: " << error.what() << '\n';
    return 64;
  }
}
