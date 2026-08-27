#include "process_runner.hpp"

#include <stdexcept>

namespace systems_course::week01 {

ProcessResult run_process(const std::string& executable,
                          const std::vector<std::string>& arguments) {
  (void)executable;
  (void)arguments;

  // TODO: Add a _WIN32 branch and a POSIX branch. Keep all platform types and
  // resource ownership inside this translation unit. See the lab README for the
  // required observable behavior and deadlock warning.
  throw std::logic_error("TODO: implement run_process");
}

}  // namespace systems_course::week01

