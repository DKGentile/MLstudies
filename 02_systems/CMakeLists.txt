cmake_minimum_required(VERSION 3.21)
project(systems_phase0 LANGUAGES CXX)

include(CTest)
find_package(Threads REQUIRED)

function(systems_target target)
  target_compile_features(${target} PRIVATE cxx_std_17)
  if(MSVC)
    target_compile_options(${target} PRIVATE /W4 /permissive-)
  else()
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
  endif()
endfunction()

# Week 1: child process contract.
add_library(systems_week01_lib
  week01_processes/starter/process_runner.cpp
)
target_include_directories(systems_week01_lib PUBLIC week01_processes/include)
target_link_libraries(systems_week01_lib PUBLIC Threads::Threads)
systems_target(systems_week01_lib)

add_executable(systems_child_probe week01_processes/probe/child_probe.cpp)
systems_target(systems_child_probe)

add_executable(systems_week01_tests week01_processes/tests/process_runner_tests.cpp)
target_include_directories(systems_week01_tests PRIVATE common)
target_link_libraries(systems_week01_tests PRIVATE systems_week01_lib)
add_dependencies(systems_week01_tests systems_child_probe)
systems_target(systems_week01_tests)
add_test(NAME systems_week01_tests
  COMMAND systems_week01_tests $<TARGET_FILE:systems_child_probe>
)
set_tests_properties(systems_week01_tests PROPERTIES TIMEOUT 10)

# Week 2: address-space and page-touch contract.
add_library(systems_week02_lib
  week02_address_spaces/starter/address_space.cpp
)
target_include_directories(systems_week02_lib PUBLIC week02_address_spaces/include)
systems_target(systems_week02_lib)

add_executable(systems_address_probe week02_address_spaces/probe/address_probe.cpp)
target_link_libraries(systems_address_probe PRIVATE systems_week02_lib Threads::Threads)
systems_target(systems_address_probe)

add_executable(systems_week02_tests week02_address_spaces/tests/address_space_tests.cpp)
target_include_directories(systems_week02_tests PRIVATE common)
target_link_libraries(systems_week02_tests PRIVATE systems_week02_lib)
systems_target(systems_week02_tests)
add_test(NAME systems_week02_tests COMMAND systems_week02_tests)

# Week 3: the bounded queue is a template starter, so the tests instantiate it.
add_executable(systems_week03_tests week03_threads_locks/tests/bounded_queue_tests.cpp)
target_include_directories(systems_week03_tests PRIVATE
  common
  week03_threads_locks/starter
)
target_link_libraries(systems_week03_tests PRIVATE Threads::Threads)
systems_target(systems_week03_tests)
add_test(NAME systems_week03_tests COMMAND systems_week03_tests)
set_tests_properties(systems_week03_tests PROPERTIES TIMEOUT 10)

# Week 4: applied bounded worker pipeline.
add_library(systems_week04_lib week04_integration/starter/frame_pipeline.cpp)
target_include_directories(systems_week04_lib PUBLIC
  week04_integration/include
  week03_threads_locks/starter
)
target_link_libraries(systems_week04_lib PUBLIC Threads::Threads)
systems_target(systems_week04_lib)

add_executable(systems_week04_tests week04_integration/tests/frame_pipeline_tests.cpp)
target_include_directories(systems_week04_tests PRIVATE common)
target_link_libraries(systems_week04_tests PRIVATE systems_week04_lib)
systems_target(systems_week04_tests)
add_test(NAME systems_week04_tests COMMAND systems_week04_tests)
set_tests_properties(systems_week04_tests PROPERTIES TIMEOUT 10)
