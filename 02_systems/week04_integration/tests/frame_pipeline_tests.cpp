#include "frame_pipeline.hpp"
#include "test_support.hpp"

#include <stdexcept>
#include <vector>

using systems_course::week04::Frame;
using systems_course::week04::FrameResult;
using systems_course::week04::process_frames;

int main() {
  course_test::Suite suite;

  suite.run("pipeline preserves input order across multiple workers", [] {
    const std::vector<Frame> frames{
        {10, {3, -2, 8, 1}},
        {4, {100}},
        {10, {}},
        {99, {-9, -1, -5}},
    };
    const auto report = process_frames(frames, 3, 2);
    const std::vector<FrameResult> expected{
        {10, 10}, {4, 0}, {10, 0}, {99, 8}};
    COURSE_CHECK(report.worker_count == 3U);
    COURSE_CHECK(report.queue_capacity == 2U);
    COURSE_CHECK(report.results == expected);
  });

  suite.run("empty input completes without inventing work", [] {
    const auto report = process_frames({}, 2, 1);
    COURSE_CHECK(report.worker_count == 2U);
    COURSE_CHECK(report.queue_capacity == 1U);
    COURSE_CHECK(report.results.empty());
  });

  suite.run("zero workers or capacity is rejected", [] {
    bool rejected_workers = false;
    bool rejected_capacity = false;
    try {
      (void)process_frames({}, 0, 1);
    } catch (const std::invalid_argument&) {
      rejected_workers = true;
    }
    try {
      (void)process_frames({}, 1, 0);
    } catch (const std::invalid_argument&) {
      rejected_capacity = true;
    }
    COURSE_CHECK(rejected_workers);
    COURSE_CHECK(rejected_capacity);
  });

  return suite.finish();
}

