cmake_minimum_required(VERSION 3.21)
project(systems_phase0 LANGUAGES CXX)

include(CTest)
find_package(Threads REQUIRED)

option(MLSTUDIES_BUILD_BUG_CLINICS
  "Expose intentional-bug clinic targets (never part of the default build/test)"
  OFF
)
set(MLSTUDIES_SANITIZER "" CACHE STRING
  "Optional sanitizer: address, address-undefined, or thread"
)
set_property(CACHE MLSTUDIES_SANITIZER PROPERTY STRINGS
  "" address address-undefined thread
)

set(_mlstudies_sanitizers "" address address-undefined thread)
if(NOT MLSTUDIES_SANITIZER IN_LIST _mlstudies_sanitizers)
  message(FATAL_ERROR
    "Unsupported MLSTUDIES_SANITIZER='${MLSTUDIES_SANITIZER}'. "
    "Choose address, address-undefined, thread, or leave it empty."
  )
endif()

if(MSVC AND (MLSTUDIES_SANITIZER STREQUAL "address-undefined" OR
             MLSTUDIES_SANITIZER STREQUAL "thread"))
  message(FATAL_ERROR
    "MSVC supports the course's address preset only. Use Linux/WSL with "
    "GCC or Clang for UndefinedBehaviorSanitizer and ThreadSanitizer."
  )
endif()

if(MLSTUDIES_SANITIZER STREQUAL "thread" AND
   NOT CMAKE_SYSTEM_NAME STREQUAL "Linux")
  message(FATAL_ERROR
    "The ThreadSanitizer clinic is supported only on Linux/WSL."
  )
endif()

function(systems_target target)
  target_compile_features(${target} PRIVATE cxx_std_17)
  if(MSVC)
    target_compile_options(${target} PRIVATE /W4 /permissive-)
  else()
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
  endif()

  if(MLSTUDIES_SANITIZER)
    if(MSVC)
      if(CMAKE_GENERATOR MATCHES "^Visual Studio")
        set_property(TARGET ${target} PROPERTY VS_GLOBAL_EnableASAN "true")
        get_target_property(_systems_target_type ${target} TYPE)
        if(_systems_target_type STREQUAL "EXECUTABLE")
          set_property(TARGET ${target} PROPERTY
            VS_GLOBAL_CopyAsanBinariesToOutDir "true"
          )
        endif()
      else()
        target_compile_options(${target} PRIVATE /fsanitize=address /Zi)
      endif()
      target_link_options(${target} PRIVATE /INCREMENTAL:NO)
    else()
      if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang|AppleClang")
        message(FATAL_ERROR
          "MLSTUDIES_SANITIZER requires MSVC, GCC, or Clang; found "
          "${CMAKE_CXX_COMPILER_ID}."
        )
      endif()
      if(MLSTUDIES_SANITIZER STREQUAL "address")
        set(_sanitizer_flags -fsanitize=address)
      elseif(MLSTUDIES_SANITIZER STREQUAL "address-undefined")
        set(_sanitizer_flags
          -fsanitize=address,undefined
          -fno-sanitize-recover=all
        )
      else()
        set(_sanitizer_flags -fsanitize=thread)
      endif()
      target_compile_options(${target} PRIVATE
        ${_sanitizer_flags} -fno-omit-frame-pointer
      )
      target_link_options(${target} PRIVATE ${_sanitizer_flags})
    endif()
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

# Intentional race: opt in explicitly, build it by name, and run it manually.
# It is deliberately absent from both the default ALL target and CTest.
if(MLSTUDIES_BUILD_BUG_CLINICS)
  add_executable(systems_race_clinic EXCLUDE_FROM_ALL
    week03_threads_locks/debugging/racy_metrics.cpp
  )
  target_link_libraries(systems_race_clinic PRIVATE Threads::Threads)
  systems_target(systems_race_clinic)
endif()

# Week 4 supplied infrastructure: native socket ownership stays out of learner
# protocol code and public platform-independent contracts.
add_library(systems_week04_tcp_support
  week04_integration/infrastructure/tcp_socket.cpp
)
target_include_directories(systems_week04_tcp_support PUBLIC
  week04_integration/include
)
if(WIN32)
  target_link_libraries(systems_week04_tcp_support PUBLIC ws2_32)
endif()
systems_target(systems_week04_tcp_support)

# Week 4: in-memory pipeline, stream framing, and TCP-to-worker integration.
add_library(systems_week04_lib
  week04_integration/starter/frame_pipeline.cpp
  week04_integration/starter/frame_protocol.cpp
  week04_integration/starter/tcp_pipeline.cpp
)
target_include_directories(systems_week04_lib PUBLIC
  week04_integration/include
  week03_threads_locks/starter
)
target_link_libraries(systems_week04_lib PUBLIC
  systems_week04_tcp_support
  Threads::Threads
)
systems_target(systems_week04_lib)

add_executable(systems_week04_tests week04_integration/tests/frame_pipeline_tests.cpp)
target_include_directories(systems_week04_tests PRIVATE common)
target_link_libraries(systems_week04_tests PRIVATE systems_week04_lib)
systems_target(systems_week04_tests)
add_test(NAME systems_week04_tests COMMAND systems_week04_tests)
set_tests_properties(systems_week04_tests PROPERTIES TIMEOUT 10)

add_executable(systems_week04_protocol_tests
  week04_integration/tests/frame_protocol_tests.cpp
)
target_include_directories(systems_week04_protocol_tests PRIVATE common)
target_link_libraries(systems_week04_protocol_tests PRIVATE systems_week04_lib)
systems_target(systems_week04_protocol_tests)
add_test(NAME systems_week04_protocol_tests COMMAND systems_week04_protocol_tests)
set_tests_properties(systems_week04_protocol_tests PROPERTIES TIMEOUT 10)

# This focused test verifies the supplied RAII Winsock/POSIX layer without
# depending on unsolved learner protocol or pipeline code.
add_executable(systems_week04_socket_tests
  week04_integration/tests/tcp_socket_tests.cpp
)
target_include_directories(systems_week04_socket_tests PRIVATE common)
target_link_libraries(systems_week04_socket_tests PRIVATE
  systems_week04_tcp_support
  Threads::Threads
)
systems_target(systems_week04_socket_tests)
add_test(NAME systems_week04_socket_tests COMMAND systems_week04_socket_tests)
set_tests_properties(systems_week04_socket_tests PROPERTIES TIMEOUT 10)

add_executable(systems_week04_tcp_tests
  week04_integration/tests/tcp_pipeline_tests.cpp
)
target_include_directories(systems_week04_tcp_tests PRIVATE common)
target_link_libraries(systems_week04_tcp_tests PRIVATE systems_week04_lib)
systems_target(systems_week04_tcp_tests)
add_test(NAME systems_week04_tcp_tests COMMAND systems_week04_tcp_tests)
set_tests_properties(systems_week04_tcp_tests PROPERTIES TIMEOUT 15)

add_executable(systems_fake_sensor week04_integration/probe/fake_sensor.cpp)
target_link_libraries(systems_fake_sensor PRIVATE systems_week04_lib)
systems_target(systems_fake_sensor)

add_executable(systems_tcp_receiver week04_integration/probe/tcp_receiver.cpp)
target_link_libraries(systems_tcp_receiver PRIVATE systems_week04_lib)
systems_target(systems_tcp_receiver)
