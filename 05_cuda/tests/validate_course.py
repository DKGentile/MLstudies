#!/usr/bin/env python3
"""CPU-only structural checks for Chapter 05.

This intentionally does not decide whether learner kernels are correct. Their
CUDA harnesses do that on a GPU. It catches accidental removal of exercises,
references, and the explicit no-CUDA path.
"""

from __future__ import annotations

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class CourseStructureTests(unittest.TestCase):
    def test_expected_labs_exist(self) -> None:
        labs = [
            "01_vector_add",
            "02_indexing_2d",
            "03_reduction",
            "04_histogram",
            "05_box_blur",
        ]
        for lab in labs:
            with self.subTest(lab=lab):
                self.assertTrue((ROOT / lab / "README.md").is_file())
                self.assertTrue((ROOT / lab / "main.cu").is_file())
                self.assertTrue((ROOT / lab / "CMakeLists.txt").is_file())

    def test_kernels_remain_learner_exercises(self) -> None:
        sources = sorted(ROOT.glob("[0-9][0-9]_*/*.cu"))
        self.assertEqual(5, len(sources))
        for source in sources:
            with self.subTest(source=str(source.relative_to(ROOT))):
                text = source.read_text(encoding="utf-8")
                self.assertIn("TODO(learner)", text)
                self.assertIn("median_kernel_ms", text)
                self.assertTrue(
                    "check_close" in text or ("PASS:" in text and "FAIL:" in text),
                    "each lab must have an explicit correctness gate",
                )
                self.assertIn("return 2", text)

    def test_no_cuda_path_is_documented_and_configurable(self) -> None:
        cmake = (ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("MLSTUDIES_ENABLE_CUDA", cmake)
        self.assertIn("check_language(CUDA)", cmake)
        self.assertIn("MLSTUDIES_ENABLE_CUDA=OFF", readme)

    def test_two_gpu_toolchain_boundary_is_explicit(self) -> None:
        cmake = (ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for token in ("sm_61", "sm_120", "CUDA 12.8", "CUDA 13"):
            self.assertIn(token, readme)
        self.assertIn("VERSION_GREATER_EQUAL 13.0", cmake)
        self.assertIn("VERSION_LESS 12.8", cmake)
        self.assertIn("${PROJECT_SOURCE_DIR}/common", cmake)

    def test_support_has_explicit_timing_boundaries(self) -> None:
        support = (ROOT / "common" / "lab_support.cuh").read_text(encoding="utf-8")
        for token in (
            "cudaEventRecord",
            "cudaEventSynchronize",
            "cudaEventElapsedTime",
            "cudaDeviceSynchronize",
        ):
            self.assertIn(token, support)


if __name__ == "__main__":
    unittest.main(verbosity=2)
