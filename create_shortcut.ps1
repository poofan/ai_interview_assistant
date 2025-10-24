# Создание ярлыка Hintsage на рабочем столе
$WshShell = New-Object -ComObject WScript.Shell

# Ярлык для SILENT запуска (без консоли)
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Hintsage AI.lnk")
$Shortcut.TargetPath = "$PSScriptRoot\start_silent.vbs"
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "Hintsage AI Interview Assistant (GPU, без консоли)"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,244"
$Shortcut.Save()

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "[OK] Ярлык создан на рабочем столе!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📁 Файл: Hintsage AI.lnk" -ForegroundColor Yellow
Write-Host "🚀 Режим: Без консоли (невидимый запуск)" -ForegroundColor Yellow
Write-Host "⚡ GPU: CUDA + faster-whisper" -ForegroundColor Yellow
Write-Host ""
Write-Host "Теперь можно запускать двойным кликом!" -ForegroundColor Green
Write-Host "Приложение запустится в фоне без окна консоли" -ForegroundColor Green
Write-Host ""
pause

