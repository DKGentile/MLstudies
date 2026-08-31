# Building on Windows, Linux, and macOS

The course uses only the C++17 standard library.

## Toolchain

- Windows: Visual Studio Build Tools with the **Desktop development with C++**
  workload, then run from a Developer PowerShell; or use a recent LLVM/MinGW
  toolchain. The optional MSVC clinic route also needs the C++ AddressSanitizer
  component selected in the Visual Studio Installer.
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
MSBuild, NMake, or Ninja executes the generated build graph, and the Windows SDK
supplies headers and libraries. Installing Visual Studio does not put all of
those tools and paths into every shell globally. A Visual Studio developer shell
initializes `PATH`, `INCLUDE`, `LIB`, and related variables for one process and
its children.

CMake also has two distinct stages:

1. **Configure/generate:** `cmake --preset default` selects a compiler and a
   generator and writes their locations into `build/CMakeCache.txt`.
2. **Build:** `cmake --build --preset default` reads that generated build tree
   and invokes its build tool.

The preset does not force one generator. CMake may select a Visual Studio
generator, or a developer may explicitly choose NMake or Ninja. The selected
generator is recorded in `build/CMakeCache.txt`; `cmake --build` must be able to
find that generator's build tool. An ordinary Git Bash process can find CMake
but does not automatically inherit the MSVC developer environment, which can
produce `no such file or directory` when CMake tries to start `nmake` or another
MSVC tool.

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

The required ownership exercise is independently targetable while Weeks 2-4
remain unfinished:

```text
cmake --build --preset default --target cpp_owned_buffer_tests
ctest --test-dir build -C Debug -R cpp_owned_buffer --output-on-failure
```

Its assertions begin red. A compiler/link failure is a scaffold problem; a
reported `TODO` or failed contract is learner work.

## Debuggers and opt-in sanitizers

The programs in `debugging_clinics/` contain intentional undefined behavior.
They are hidden behind `MLSTUDIES_BUILD_BUG_CLINICS`, excluded from the default
build, and never registered with CTest.

Use the plain debug preset for breakpoints, stepping, locals, and call stacks:

```text
cmake --preset debug-clinics
cmake --build --preset debug-clinics
```

Use a distinct build tree for AddressSanitizer:

```text
cmake --preset asan
cmake --build --preset asan
```

After implementing `OwnedBuffer`, instrument its contract target too:

```text
cmake --build --preset asan --target cpp_owned_buffer_tests
ctest --test-dir build/asan -C RelWithDebInfo -R cpp_owned_buffer --output-on-failure
```

For GCC/Clang on Linux, macOS, or WSL, the combined address/undefined route is:

```text
cmake --preset asan-ubsan
cmake --build --preset asan-ubsan
```

The executable path printed by the build depends on the generator. Visual
Studio normally adds a `Debug/` or `RelWithDebInfo/` directory; Ninja/Makefiles
normally do not. Run one clinic binary at a time and expect a nonzero sanitizer
exit before repair.

With a Visual Studio generator, the project uses Visual Studio's native ASan
integration and copies the compiler-matched sanitizer runtime DLL beside each
instrumented executable. Other MSVC generators require a Developer PowerShell
so that runtime is on `PATH`. An immediate exit or missing-DLL dialog with no
ASan report is a loader/toolchain symptom, not a clean diagnostic run.

| Toolchain/host | Supported course route | Honest limitation |
|---|---|---|
| MSVC on Windows 10+ x86/x64 | `/fsanitize=address` through preset `asan` | MSVC does not provide UBSan or TSan. ASan conflicts with Edit-and-Continue `/ZI`, `/RTC1`, and incremental linking, so the preset uses `RelWithDebInfo` and disables incremental linking. |
| GCC/Clang on Linux or WSL | ASan, UBSan, or TSan in separate build trees | ASan+UBSan may run together; TSan must not be combined with ASan. The race clinic is in the systems module. |
| AppleClang on macOS | ASan+UBSan when the installed compiler runtime provides them | Platform behavior is not evidence that a Windows- or Linux-only route was tested. |
| Native Windows GCC/Clang distributions | only when that distribution includes the requested sanitizer runtime | The course does not treat an unrelated `clang++` found on `PATH` as proof that compiler-rt is installed. Use MSVC ASan or the documented WSL route. |

`MLSTUDIES_SANITIZER` accepts `address`, `address-undefined`, or `thread`.
Unsupported compiler/host combinations stop at configure time with a specific
message. ASan and TSan are separate configurations because their runtimes and
instrumentation cannot be combined.

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
