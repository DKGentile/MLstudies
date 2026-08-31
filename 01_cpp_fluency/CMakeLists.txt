cmake_minimum_required(VERSION 3.21)
project(cpp_fluency_phase0 LANGUAGES CXX)

include(CTest)

option(MLSTUDIES_BUILD_BUG_CLINICS
  "Expose intentional debugging-clinic targets (never added to CTest)" OFF
)
set(MLSTUDIES_SANITIZER "" CACHE STRING
  "Opt-in sanitizer: address, address-undefined, or thread"
)
set_property(CACHE MLSTUDIES_SANITIZER PROPERTY STRINGS
  "" address address-undefined thread
)

function(course_sanitizer target)
  if(MLSTUDIES_SANITIZER STREQUAL "")
    return()
  endif()

  if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    if(NOT MLSTUDIES_SANITIZER STREQUAL "address")
      message(FATAL_ERROR
        "MSVC supports AddressSanitizer for these labs, but not "
        "MLSTUDIES_SANITIZER=${MLSTUDIES_SANITIZER}. Use GCC or Clang in "
        "Linux/WSL for UndefinedBehaviorSanitizer or ThreadSanitizer."
      )
    endif()

    if(CMAKE_GENERATOR MATCHES "^Visual Studio")
      # Use the Visual Studio C++ targets so the compiler flag and its matching
      # runtime DLL are managed as one toolchain feature. Static libraries are
      # instrumented, but only runnable targets need runtime deployment.
      set_property(TARGET ${target} PROPERTY VS_GLOBAL_EnableASAN true)
      get_target_property(_course_target_type ${target} TYPE)
      if(_course_target_type STREQUAL "EXECUTABLE")
        # This makes the executable launchable from an ordinary shell without
        # a global PATH mutation.
        set_property(TARGET ${target} PROPERTY
          VS_GLOBAL_CopyAsanBinariesToOutDir true
        )
      endif()
    else()
      target_compile_options(${target} PRIVATE /fsanitize=address /Zi)
    endif()
    target_link_options(${target} PRIVATE /INCREMENTAL:NO)
    return()
  endif()

  if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang|AppleClang")
    message(FATAL_ERROR
      "MLSTUDIES_SANITIZER requires MSVC, GCC, Clang, or AppleClang; found "
      "${CMAKE_CXX_COMPILER_ID}."
    )
  endif()

  if(MLSTUDIES_SANITIZER STREQUAL "address")
    set(sanitizer_flags -fsanitize=address -fno-omit-frame-pointer)
  elseif(MLSTUDIES_SANITIZER STREQUAL "address-undefined")
    set(sanitizer_flags
      -fsanitize=address,undefined
      -fno-omit-frame-pointer
      -fno-sanitize-recover=all
    )
  elseif(MLSTUDIES_SANITIZER STREQUAL "thread")
    if(WIN32)
      message(FATAL_ERROR
        "ThreadSanitizer is not a supported native-Windows route for this "
        "course. Configure this preset under Linux/WSL with GCC or Clang."
      )
    endif()
    set(sanitizer_flags -fsanitize=thread -fno-omit-frame-pointer)
  else()
    message(FATAL_ERROR
      "Unknown MLSTUDIES_SANITIZER='${MLSTUDIES_SANITIZER}'. Expected "
      "address, address-undefined, thread, or an empty value."
    )
  endif()

  target_compile_options(${target} PRIVATE ${sanitizer_flags})
  target_link_options(${target} PRIVATE ${sanitizer_flags})
endfunction()

function(course_target target)
  target_compile_features(${target} PRIVATE cxx_std_17)
  if(MSVC)
    target_compile_options(${target} PRIVATE /W4 /permissive-)
  else()
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic)
  endif()
  course_sanitizer(${target})
endfunction()

function(add_course_week week slug)
  set(lib "cpp_${week}_lib")
  set(test "cpp_${week}_tests")

  add_library(${lib} "${slug}/starter/${week}.cpp")
  target_include_directories(${lib} PUBLIC "${slug}/include")
  course_target(${lib})

  add_executable(${test} "${slug}/tests/${week}_tests.cpp")
  target_include_directories(${test} PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/common")
  target_link_libraries(${test} PRIVATE ${lib})
  course_target(${test})

  add_test(NAME ${test} COMMAND ${test})
endfunction()

add_course_week(week01 week01_arrays_hash_two_pointers)
add_course_week(week02 week02_binary_search_sliding_window)
add_course_week(week03 week03_stacks_heaps_intervals)
add_course_week(week04 week04_trees_graphs)

# Required Weeks 2-4 Modern C++ engineering supplement.
add_library(cpp_owned_buffer_lib
  modern_cpp_engineering/starter/owned_buffer.cpp
)
target_include_directories(cpp_owned_buffer_lib PUBLIC
  modern_cpp_engineering/include
)
course_target(cpp_owned_buffer_lib)

add_executable(cpp_owned_buffer_tests
  modern_cpp_engineering/tests/owned_buffer_tests.cpp
)
target_include_directories(cpp_owned_buffer_tests PRIVATE common)
target_link_libraries(cpp_owned_buffer_tests PRIVATE cpp_owned_buffer_lib)
course_target(cpp_owned_buffer_tests)
add_test(NAME cpp_owned_buffer_tests COMMAND cpp_owned_buffer_tests)

# These programs contain deliberate undefined behavior. They are absent unless
# explicitly requested, excluded from the normal build, and never registered
# with CTest so an ordinary course build cannot look accidentally broken.
if(MLSTUDIES_BUILD_BUG_CLINICS)
  add_executable(cpp_lifetime_bug_clinic EXCLUDE_FROM_ALL
    debugging_clinics/lifetime_bug.cpp
  )
  course_target(cpp_lifetime_bug_clinic)

  add_executable(cpp_bounds_bug_clinic EXCLUDE_FROM_ALL
    debugging_clinics/bounds_bug.cpp
  )
  course_target(cpp_bounds_bug_clinic)
endif()
