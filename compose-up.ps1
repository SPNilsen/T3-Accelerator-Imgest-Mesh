# compose-up.ps1 — Imgest-Mesh compose wrapper for Windows
#
# docker-compose.exe is installed via Chocolatey but the shim failed (lib-bad),
# so it is not on PATH. This script calls it directly.
#
# Usage:
#   .\compose-up.ps1              # build + up (default)
#   .\compose-up.ps1 -Down        # stop and remove containers
#   .\compose-up.ps1 -Rebuild     # down + build + up (full restart)
#   .\compose-up.ps1 -Logs        # tail logs after starting
#
# SSL bypass (corporate Netskope proxy):
#   Set SKIP_SSL_VERIFY=true in .env before running, or:
#   $env:SKIP_SSL_VERIFY = "true"; .\compose-up.ps1 -Rebuild

param(
    [switch]$Down,
    [switch]$Rebuild,
    [switch]$Logs
)

$dc = "C:\ProgramData\chocolatey\lib-bad\docker-compose\5.1.3\tools\docker-compose.exe"

if (-not (Test-Path $dc)) {
    Write-Error "docker-compose.exe not found at: $dc"
    Write-Host "Install via: choco install docker-compose"
    exit 1
}

$services = "camera", "orchestrator", "inference", "webserver", "docs"

if ($Down -or $Rebuild) {
    Write-Host "Stopping containers..." -ForegroundColor Cyan
    & $dc down
}

if (-not $Down) {
    Write-Host "Building images..." -ForegroundColor Cyan
    & $dc build @services
    if (-not $?) { Write-Error "Build failed."; exit 1 }

    Write-Host "Starting services..." -ForegroundColor Cyan
    & $dc up -d @services
    if (-not $?) { Write-Error "Up failed."; exit 1 }

    Write-Host ""
    Write-Host "Services running:" -ForegroundColor Green
    & $dc ps
}

if ($Logs) {
    & $dc logs -f @services
}
