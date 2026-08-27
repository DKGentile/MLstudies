[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("ncu", "nsys")]
    [string]$Tool,

    [Parameter(Mandatory = $true)]
    [string]$Executable,

    [string]$Kernel = "regex:.*",
    [ValidateRange(0, 2147483647)]
    [int]$LaunchSkip = 0,
    [string]$OutputName = "profile",
    [string]$OutputDirectory = (Join-Path $PSScriptRoot "..\profiles"),

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ProgramArgs
)

$profiler = Get-Command $Tool -ErrorAction SilentlyContinue
if ($null -eq $profiler) {
    Write-Warning "$Tool is not installed or not on PATH; profiling was skipped."
    exit 0
}

if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
    Write-Error "Executable not found: $Executable"
    exit 2
}

$resolvedExecutable = (Resolve-Path -LiteralPath $Executable).Path
$null = New-Item -ItemType Directory -Path $OutputDirectory -Force
$resolvedOutputDirectory = (Resolve-Path -LiteralPath $OutputDirectory).Path
$outputBase = Join-Path $resolvedOutputDirectory $OutputName

Write-Host "Profiler: $($profiler.Source)"
Write-Host "Executable: $resolvedExecutable"
Write-Host "Output base: $outputBase"

if ($Tool -eq "ncu") {
    & $profiler.Source `
        --set full `
        --target-processes all `
        --kernel-name-base function `
        --kernel-name $Kernel `
        --launch-skip $LaunchSkip `
        --launch-count 1 `
        --force-overwrite `
        --export $outputBase `
        $resolvedExecutable @ProgramArgs
} else {
    & $profiler.Source profile `
        --stats true `
        --force-overwrite true `
        --output $outputBase `
        $resolvedExecutable @ProgramArgs
}

exit $LASTEXITCODE
