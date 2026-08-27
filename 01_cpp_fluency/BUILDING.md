# Building on Windows, Linux, and macOS

The course uses only the C++17 standard library.

## Toolchain

- Windows: Visual Studio Build Tools with the **Desktop development with C++**
  workload, then run from a Developer PowerShell; or use a recent LLVM/MinGW
  toolchain.
- Ubuntu/Debian: `build-essential` and CMake 3.21 or newer.
- macOS: Xcode Command Line Tools and CMake.

Confirm the tools before beginning:

```text
cmake --version
g++ --version       # GCC, or
clang++ --version   # Clang, or
cl                  # MSVC Developer shell
```

## Understand the Windows toolchain environment

VS Code is the editor. MSVC is a separate toolchain: `cl.exe` compiles,
`nmake.exe` executes this build graph, and the Windows SDK supplies headers and
libraries. Installing Visual Studio Build Tools does not put all of those tools
and paths into every shell globally. A Visual Studio developer shell initializes
`PATH`, `INCLUDE`, `LIB`, and related variables for one process and its children.

CMake also has two distinct stages:

1. **Configure/generate:** `cmake --preset default` selects a compiler and a
   generator and writes their locations into `build/CMakeCache.txt`.
2. **Build:** `cmake --build --preset default` reads that generated build tree
   and invokes its build tool.

This module's current Windows build tree uses the `NMake Makefiles` generator.
Consequently, `cmake --build` must be able to find `nmake.exe`. An ordinary Git
Bash process can find CMake but does not automatically inherit the MSVC
developer environment, which produces `no such file or directory` when CMake
tries to start `nmake`.

### MSVC from VS Code

The workspace defines an **MSVC Developer PowerShell** terminal profile. Reload
the VS Code window, open a new terminal, and verify the environment instead of
assuming it is active:

```powershell
Get-Command cl,nmake,cmake
```

Existing terminal processes do not gain a newly configured environment. In the
new developer terminal, run the CMake commands below directly.

### MSVC while keeping Git Bash

Environment variables are inherited by child processes. Start Git Bash from an
initialized Developer PowerShell:

```powershell
& 'C:\Program Files\Git\bin\bash.exe' --login
```

Then verify the inherited toolchain from Bash:

```bash
command -v cl
command -v nmake
command -v cmake
```

This is still the MSVC toolchain; Bash is only the command interpreter. A native
MinGW, MSYS2, or WSL compiler is a different toolchain and should use a separate
CMake preset and build directory. Never reuse one CMake build tree across
different generators or compilers.

## CMake workflow

Run from `01_cpp_fluency`:

```text
cmake --preset default
cmake --build --preset default
ctest --preset default
```

The warning level is `/W4 /permissive-` on MSVC and
`-Wall -Wextra -Wpedantic` on GCC/Clang.

## One-file feedback loop

When you want the shortest possible GCC/Clang loop for week 1:

```text
g++ -std=c++17 -Wall -Wextra -Wpedantic -Icommon -Iweek01_arrays_hash_two_pointers/include week01_arrays_hash_two_pointers/starter/week01.cpp week01_arrays_hash_two_pointers/tests/week01_tests.cpp -o week01_tests
./week01_tests
```

Use the CMake flow for normal work because it handles all platforms and weeks.

The convenience PowerShell script is local, readable course code. If the host's
execution policy blocks it, invoke it for that process only:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_checks.ps1
```

## What an initial failure means

An untouched exercise generally reports a message such as
`TODO: implement two_sum_indices`. Implement one function at a time and rerun
the same test binary. A crash, sanitizer error, or hang is not an acceptable
substitute for a deliberate failing assertion.
