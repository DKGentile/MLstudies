"""Fast checks that should pass before any exercise is implemented."""

from __future__ import annotations

import importlib

import pytest


MODULES = (
    "numpy_fluency",
    "linear_regression",
    "logistic_regression",
    "gradient_checks",
    "regularization",
    "two_layer_net",
)


@pytest.mark.parametrize("module_name", MODULES)
def test_exercise_module_imports(module_name: str) -> None:
    module = importlib.import_module(f"ml_fundamentals.{module_name}")
    assert module.__doc__


def test_gradient_result_is_a_readable_value_object() -> None:
    from ml_fundamentals.gradient_checks import GradientCheckResult

    assert set(GradientCheckResult.__dataclass_fields__) == {
        "passed",
        "relative_error",
        "numeric",
        "analytic",
    }
