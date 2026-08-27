param(
    [string]$Pattern = ""
)

$ErrorActionPreference = "Stop"
$ModuleRoot = Split-Path -Parent $PSScriptRoot

if (-not (Get-Command cmake -ErrorAction SilentlyContinue)) {
    throw "CMake was not found. Install CMake and a C++17 compiler before running the labs."
}

Push-Location $ModuleRoot
try {
    cmake --preset default
    if ($LASTEXITCODE -ne 0) { throw "CMake configure failed with exit code $LASTEXITCODE." }
    cmake --build --preset default
    if ($LASTEXITCODE -ne 0) { throw "CMake build failed with exit code $LASTEXITCODE." }
    if ($Pattern) {
        ctest --test-dir build -C Debug -R $Pattern --output-on-failure
    }
    else {
        ctest --preset default
    }
    if ($LASTEXITCODE -ne 0) { throw "CTest failed with exit code $LASTEXITCODE." }
}
finally {
    Pop-Location
}
