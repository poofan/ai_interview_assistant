@echo off
echo ========================================
echo   E2E Testing - All Services
echo ========================================
echo.

echo [1] Checking Backend API (localhost:8000)...
timeout /t 2 /nobreak >nul
curl http://localhost:8000/health 2>nul
if errorlevel 1 (
    echo    Backend NOT running
) else (
    echo    Backend OK
)

echo.
echo [2] Checking Backend API Docs...
echo    Open in browser: http://localhost:8000/docs

echo.
echo [3] Checking Frontend (localhost:3000)...
curl http://localhost:3000 2>nul | findstr /C:"Hintsage" >nul
if errorlevel 1 (
    echo    Frontend NOT running or not ready
) else (
    echo    Frontend OK
)

echo.
echo [4] Checking Desktop App...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Hintsage*" 2>nul | find "python.exe" >nul
if errorlevel 1 (
    echo    Desktop App NOT running
) else (
    echo    Desktop App OK
)

echo.
echo ========================================
echo   Test Summary
echo ========================================
echo.
echo Services:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   Desktop:  Check system tray
echo.
echo Next steps:
echo   1. Open http://localhost:3000 in browser
echo   2. Check http://localhost:8000/docs for API
echo   3. Test Desktop App with Ctrl+Shift+Q
echo.
pause


