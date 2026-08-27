#!/usr/bin/env python3
"""CPU-only structural checks for the GPU optimization chapter."""

from __future__ import annotations

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class OptimizationCourseTests(unittest.TestCase):
    def test_expected_stages_exist(self) -> None:
        stages = [
            "01_coalescing",
            "02_tiled_blur",
            "03_privatized_histogram",
        ]
        for stage in stages:
            with self.subTest(stage=stage):
                self.assertTrue((ROOT / stage / "README.md").is_file())
                self.assertTrue((ROOT / stage / "main.cu").is_file())
                self.assertTrue((ROOT / stage / "CMakeLists.txt").is_file())

    def test_optimized_kernels_are_not_filled_in(self) -> None:
        required_todos = {
            "02_tiled_blur/main.cu": "tiled_blur_kernel",
            "03_privatized_histogram/main.cu": "shared_histogram_kernel",
        }
        for relative, kernel in required_todos.items():
            with self.subTest(source=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn(kernel, text)
                self.assertIn("TODO(learner)", text)
                self.assertTrue("check_close" in text or "PASS " in text)
                self.assertIn("return 2", text)

    def test_benchmarks_have_correct_timing_primitives(self) -> None:
        support = (ROOT / "common" / "benchmark.cuh").read_text(encoding="utf-8")
        for token in (
            "cudaEventRecord",
            "cudaEventSynchronize",
            "cudaEventElapsedTime",
            "cudaDeviceSynchronize",
            "steady_clock",
            "median",
        ):
            self.assertIn(token, support)

    def test_explicit_no_cuda_path(self) -> None:
        cmake = (ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("MLSTUDIES_ENABLE_CUDA", cmake)
        self.assertIn("check_language(CUDA)", cmake)
        self.assertIn("gpu_optimization_skipped", cmake)
        self.assertIn("MLSTUDIES_ENABLE_CUDA=OFF", readme)

    def test_two_gpu_architecture_guidance_and_include_root(self) -> None:
        cmake = (ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for token in ("architecture `61`", "architecture `120`", "CUDA 13"):
            self.assertIn(token, readme)
        self.assertIn("VERSION_GREATER_EQUAL 13.0", cmake)
        self.assertIn("VERSION_LESS 12.8", cmake)
        self.assertIn("${PROJECT_SOURCE_DIR}/common", cmake)

    def test_profile_helpers_skip_missing_tools(self) -> None:
        powershell = (ROOT / "profiling" / "profile.ps1").read_text(encoding="utf-8")
        shell = (ROOT / "profiling" / "profile.sh").read_text(encoding="utf-8")
        self.assertIn("profiling was skipped", powershell)
        self.assertIn("profiling was skipped", shell)
        self.assertIn("--launch-count", powershell)
        self.assertIn("--launch-count", shell)
        self.assertIn("--launch-skip", powershell)
        self.assertIn("--launch-skip", shell)
        worksheet = (ROOT / "profiling" / "WORKSHEET.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("LaunchSkip 1", worksheet)
        self.assertIn("LAUNCH_SKIP=1", worksheet)

    def test_cross_gpu_template_names_both_targets(self) -> None:
        report = (ROOT / "results" / "BENCHMARK_TEMPLATE.md").read_text(
            encoding="utf-8"
        )
        for token in (
            "GTX 1080",
            "RTX 5060 Ti",
            "Naive kernel ms",
            "Optimized kernel ms",
            "Achieved occupancy",
            "first bottleneck",
        ):
            self.assertIn(token.lower(), report.lower())

    def test_worksheet_separates_correctness_and_timing_scope(self) -> None:
        worksheet = (ROOT / "profiling" / "WORKSHEET.md").read_text(
            encoding="utf-8"
        )
        for token in (
            "CPU reference",
            "kernel-only",
            "end-to-end",
            "hypothesis",
            "falsify",
            "occupancy",
            "shared-memory",
        ):
            self.assertIn(token.lower(), worksheet.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
