#include "process_runner.hpp"
#include "test_support.hpp"

#include <stdexcept>
#include <string>

using systems_course::week01::run_process;

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("expected path to child probe");
  }
  const std::string child_path = argv[1];
  course_test::Suite suite;

  suite.run("child exit status and both output streams are captured", [&] {
    const auto result = run_process(child_path, {"--exit", "7"});
    COURSE_CHECK(result.exit_code == 7);
    COURSE_CHECK(result.stdout_text.find("probe-out:7") != std::string::npos);
    COURSE_CHECK(result.stderr_text.find("probe-err:7") != std::string::npos);
  });

  suite.run("argument boundaries do not invoke a command shell", [&] {
    const std::string payload = "two words;not-a-command & still-one-argument";
    const auto result = run_process(child_path, {"--echo", payload});
    COURSE_CHECK(result.exit_code == 0);
    COURSE_CHECK(result.stdout_text.find("probe-out:" + payload) !=
                 std::string::npos);
    COURSE_CHECK(result.stderr_text.empty());
  });

  return suite.finish();
}

