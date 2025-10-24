# Hintsage - Hidden Launch (minimized console)
# Encoding: UTF-8

$ErrorActionPreference = "Stop"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check python.exe
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "[ERROR] python.exe not found in venv!" -ForegroundColor Red
    Write-Host "[FIX] Run install.bat first" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Start hidden process
Write-Host "[START] Launching Hintsage in background..." -ForegroundColor Green
Write-Host "[INFO] Console will be hidden" -ForegroundColor Cyan

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "$scriptPath\venv\Scripts\python.exe"
$psi.Arguments = "main.py"
$psi.WorkingDirectory = $scriptPath
$psi.WindowStyle = "Hidden"
$psi.CreateNoWindow = $true
$psi.UseShellExecute = $false

$process = [System.Diagnostics.Process]::Start($psi)

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "[OK] Hintsage started! PID: $($process.Id)" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Hotkeys (global):" -ForegroundColor Yellow
Write-Host "  Ctrl+Shift+H - Toggle window" -ForegroundColor White
Write-Host "  Ctrl+Shift+Q - Recognize speech" -ForegroundColor White
Write-Host "  Ctrl+Shift+S - Screenshot + OCR" -ForegroundColor White
Write-Host "  Ctrl+Shift+X - Exit" -ForegroundColor White
Write-Host ""
Write-Host "Logs: logs\hintsage.log" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to close this window (app continues)..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
