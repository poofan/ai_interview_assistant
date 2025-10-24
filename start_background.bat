@echo off
REM ==================================================
REM Hintsage - Запуск в фоне (БЕЗ консоли)
REM ==================================================

chcp 65001 >nul
cd /d "%~dp0"

REM Проверка python.exe
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] python.exe не найден в venv!
    echo [INFO] Путь: %CD%\venv\Scripts\python.exe
    pause
    exit /b 1
)

REM Запуск БЕЗ консоли через pythonw.exe
cls
echo.
echo ============================================================
echo [HINTSAGE] Запуск в фоновом режиме
echo ============================================================
echo.
echo [START] Запускаю Hintsage с GPU (без консоли)...
echo.
echo ⌨️  Горячие клавиши:
echo    Ctrl+Shift+H - Показать/скрыть окно
echo    Ctrl+Shift+Q - Распознать речь
echo    Ctrl+Shift+S - Скриншот + OCR
echo    Ctrl+Shift+X - Выход
echo.
echo ============================================================
echo [OK] Приложение запускается...
echo [INFO] Консоль автоматически закроется через 3 секунды
echo [INFO] Приложение продолжит работу в фоне!
echo ============================================================
timeout /t 3 /nobreak >nul

REM Запуск через python.exe в минимизированном окне
start "" /MIN venv\Scripts\python.exe main.py

REM Консоль закрывается
exit

