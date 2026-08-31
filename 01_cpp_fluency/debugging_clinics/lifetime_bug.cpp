#include <cstddef>
#include <iostream>
#include <string>
#include <string_view>

namespace {

std::string_view make_frame_label(std::size_t sequence) {
  std::string label = "frame-sequence=" + std::to_string(sequence) + ":";
  // Keep the text outside typical small-string storage so an invalid lifetime
  // is observable to a memory diagnostic rather than hidden by one library's
  // representation choice.
  label.append(128, 'x');
  return label;
}

char inspect_first_byte(std::string_view label) {
  return label.at(0);
}

}  // namespace

int main() {
  // INTENTIONAL BUG CLINIC: reproduce and explain the diagnostic before edit.
  // LEARNER TODO: repair the ownership/lifetime contract, rerun the same
  // diagnostic, and record why the repaired object remains alive long enough.
  const std::string_view label = make_frame_label(42);
  std::cout << "first byte: " << inspect_first_byte(label) << '\n';
  return 0;
}
