# Learning Resource Index

The actual assignments now live beside the exercise and checkpoint they prepare.
This file is an index, not a second syllabus. Sources are primary documentation,
official university courses, vendor engineering material, or original papers.

## Resource contract

1. Read or watch the **core before coding** item for the current unit.
2. Close it and answer the local ready-to-code check from memory.
3. Implement and run the smallest test.
4. Use an **extension after first attempt** only to explain a concrete failure,
   measurement, or completed baseline.

Worked solutions and problem editorials are intentionally delayed. API references
may stay open while coding because they define language/library contracts; they do
not replace your algorithm or derivation.

## Point-of-use map

| Course span | Preparation location |
|---|---|
| C++ Weeks 1–4 | [Week 1](../01_cpp_fluency/week01_arrays_hash_two_pointers/README.md#prepare), [Week 2](../01_cpp_fluency/week02_binary_search_sliding_window/README.md#prepare), [Week 3](../01_cpp_fluency/week03_stacks_heaps_intervals/README.md#prepare), [Week 4](../01_cpp_fluency/week04_trees_graphs/README.md#prepare), plus [Modern C++ engineering](../01_cpp_fluency/modern_cpp_engineering/README.md) |
| Debugging clinics | [C++ lifetime/bounds clinics](../01_cpp_fluency/debugging_clinics/README.md) and the Systems race clinic linked from [threads/locks](../02_systems/week03_threads_locks/README.md) |
| Systems Weeks 1–4 | [Processes](../02_systems/week01_processes/README.md#prepare), [address spaces](../02_systems/week02_address_spaces/README.md#prepare), [threads/locks](../02_systems/week03_threads_locks/README.md#prepare), [TCP bounded pipeline](../02_systems/week04_integration/README.md#prepare) |
| ML Weeks 3–6 | [Resource-by-starter table](../03_ml_fundamentals/README.md#preparation-at-the-point-of-use) |
| CV Weeks 5–9 | [Convolution/CNN and camera-geometry routes](../04_computer_vision/README.md#preparation-at-the-point-of-use) and [CIFAR-10 loop preparation](../04_computer_vision/cifar10/README.md#3-prepare-for-the-learning-loops) |
| CUDA Weeks 6–12 | [Resource-by-lab route](../05_cuda/README.md#resource-route); each lab also repeats its immediate prerequisites |
| GPU optimization Weeks 11–14 | [Resource-by-stage route](../06_gpu_optimization/README.md#resource-route); each coding stage has a local `Prepare` check |
| Capstone Weeks 10–22 | [Resource-by-milestone route](../07_edge_detect_track/README.md#prepare-by-milestone); each implementation lab narrows it locally |
| Interviews Weeks 18–26 | [Weekly preparation route](../08_interviews/README.md#weekly-preparation-route), preparation in each coding/design drill, and the non-weekly [reconnaissance protocol](../08_interviews/interview_recon.md) |

The calendar overlaps chapters. For example, Week 1's NumPy maintenance uses
ML Stop 1's indexing/broadcasting sources even though the primary build is C++.
Use [COURSE_MAP.md](../COURSE_MAP.md) to identify both the primary and parallel
work, then follow the links above.

## Full source libraries

Use these indexes when a local assignment tells you to select another explanation:

- [MIT OpenCourseWare 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines),
  [cppreference](https://en.cppreference.com/w/), Clang's
  [sanitizer documentation](https://clang.llvm.org/docs/), and Microsoft's
  [AddressSanitizer documentation](https://learn.microsoft.com/en-us/cpp/sanitizers/asan?view=msvc-170)
- [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/)
- POSIX/Linux [`socket`](https://man7.org/linux/man-pages/man7/socket.7.html) and
  [`tcp`](https://man7.org/linux/man-pages/man7/tcp.7.html) manuals, Microsoft
  [Winsock documentation](https://learn.microsoft.com/en-us/windows/win32/winsock/getting-started-with-winsock),
  and [Beej's Guide](https://beej.us/guide/bgnet/) as a focused supplement
- [Stanford CS229](https://cs229.stanford.edu/) and [CS231n](https://cs231n.github.io/)
- [NumPy user guide](https://numpy.org/doc/stable/user/) and [PyTorch tutorials](https://docs.pytorch.org/tutorials/)
- [Modern Robotics homogeneous transforms](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/),
  Stanford [CS231A camera-model notes](https://web.stanford.edu/class/cs231a/course_notes/01-camera-models.pdf),
  and OpenCV's official [camera model/calibration reference](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)
- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/) and [Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)
- [ONNX documentation](https://onnx.ai/onnx/) and [TensorRT documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/)
