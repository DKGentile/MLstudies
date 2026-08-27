# Setup

The course is intentionally layered. Install only what the current chapter needs.
Use separate host and Jetson environments; the original Jetson Nano is a legacy
platform and cannot share a modern desktop Python/CUDA stack.

## 1. Inspect the machine

```powershell
python scripts/doctor.py
```

The doctor is read-only. Missing C++, CUDA, PyTorch, or TensorRT is reported as a
capability, not a course failure.

## 2. Base Python environment

Use a virtual environment. Python 3.12 is the conservative choice for the broadest
binary-package compatibility; a newer interpreter is fine when the packages you
need publish compatible wheels.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-core.txt
```

On Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-core.txt
```

Do not blindly install a CUDA wheel from this repository. Select the command that
matches the installed driver and desired compute platform on PyTorch's official
installer page, then install [requirements-ml.txt](requirements-ml.txt).

## 3. C++ toolchain

The exercises require a C++17 compiler. Reasonable choices are:

- Windows: Visual Studio Build Tools with the “Desktop development with C++”
  workload, or WSL2 with GCC/Clang.
- Linux: GCC or Clang plus CMake and Ninja.

Each C++ chapter shows a direct compiler command as well as CMake where supplied.
Compile with warnings enabled. Add AddressSanitizer/UndefinedBehaviorSanitizer on a
platform where your compiler supports them.

## 4. CUDA host

Install the NVIDIA driver first, then a CUDA Toolkit compatible with the driver and
the code you intend to build. Confirm:

```powershell
nvidia-smi
nvcc --version
```

PyTorch wheels carry the CUDA runtime components they need; building CUDA C++ labs
still requires a local toolkit and `nvcc`. These are related but separate setups.

## 5. Optional ML and deployment packages

```powershell
python -m pip install -r requirements-ml.txt
python -m pip install -r requirements-deploy.txt
```

The deployment requirements deliberately avoid hard pins. Once a working
combination is found on a particular machine, capture exact output with:

```powershell
python -m pip freeze > progress/environment-host.txt
python scripts/doctor.py --json > progress/hardware-host.json
```

On Jetson, use NVIDIA/JetPack-compatible packages rather than reusing the host lock
file.

## 6. Verify the scaffold

```powershell
python scripts/validate_repo.py
python -m pytest -q
```

The safe-default tests should pass while learner challenges skip. Each Python
chapter documents the environment variable that enables its red tests. Native
C++/CUDA tests execute their unsolved exercises as soon as you build them.
