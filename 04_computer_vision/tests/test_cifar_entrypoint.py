from __future__ import annotations

import builtins
import importlib.util
import os
import runpy
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "cifar10" / "train.py"


def _block_ml_imports(monkeypatch: pytest.MonkeyPatch) -> None:
    real_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name == "torch" or name.startswith("torch.") or name == "torchvision":
            raise AssertionError(f"safe default unexpectedly imported {name}")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)


def test_no_argument_mode_does_not_import_ml_packages_or_write(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _block_ml_imports(monkeypatch)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [str(SCRIPT)])

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_path(str(SCRIPT), run_name="__main__")

    assert exit_info.value.code == 0
    output = capsys.readouterr().out
    assert "safe default" in output.lower()
    assert "No PyTorch import, download, training, or file write" in output
    assert not list(tmp_path.iterdir())


def test_parser_defaults_do_not_authorize_download_or_training() -> None:
    spec = importlib.util.spec_from_file_location("cifar10_starter", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    args = module.build_parser().parse_args([])

    assert not args.train
    assert not args.smoke_test
    assert not args.download


def test_smoke_mode_runs_one_forward_pass_when_explicitly_enabled(capsys) -> None:
    if os.environ.get("RUN_TORCH_SMOKE") != "1":
        pytest.skip("set RUN_TORCH_SMOKE=1 after installing compatible PyTorch")
    spec = importlib.util.spec_from_file_location("cifar10_smoke_starter", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    exit_code = module.main(["--smoke-test", "--device", "cpu"])

    assert exit_code == 0
    assert "logits=(8, 10)" in capsys.readouterr().out
