#pragma once

#include <string>
#include <vector>

namespace systems_course::week01 {

struct ProcessResult {
  int exit_code = -1;
  std::string stdout_text;
  std::string stderr_text;
};

// Launches executable directly (not through a command shell), passes each
// vector element as exactly one argument, captures stdout/stderr independently,
// waits for termination, and returns the child's exit code. Throws
// std::system_error when creation, I/O, or waiting fails.
ProcessResult run_process(const std::string& executable,
                          const std::vector<std::string>& arguments);

}  // namespace systems_course::week01

