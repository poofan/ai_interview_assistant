@echo off
REM ==================================================
REM Hintsage AI Interview Assistant - Launcher
REM Архитектура: Онтология "Ясна"
REM ==================================================

chcp 65001 >nul
cls

echo.
echo ============================================================
echo [HINTSAGE] AI Interview Assistant
echo Архитектура: Онтология "Ясна" - Функция = Архетип
echo ============================================================
echo.
echo [INFO] Запуск приложения...
echo [INFO] GPU ускорение: CUDA (faster-whisper + EasyOCR)
echo.

REM Проверка виртуального окружения
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Виртуальное окружение не найдено!
    echo [FIX] Запустите install.bat для установки
    pause
    exit /b 1
)

REM Проверка конфигурации
if not exist "config.yaml" (
    echo [WARNING] config.yaml не найден!
    echo [FIX] Копирую config.example.yaml -> config.yaml
    copy config.example.yaml config.yaml >nul
)

REM Запуск приложения через venv
echo [START] Запускаю Hintsage с GPU...
echo.
echo ⌨️  Горячие клавиши:
echo    Ctrl+Shift+H - Показать/скрыть окно
echo    Ctrl+Shift+Q - Распознать речь
echo    Ctrl+Shift+S - Скриншот + OCR
echo    Ctrl+Shift+C - Очистить контекст
echo    Ctrl+Shift+X - Выход
echo.
echo ============================================================
echo.

venv\Scripts\python.exe main.py

REM Если приложение закрылось с ошибкой
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Приложение завершилось с ошибкой (код: %ERRORLEVEL%)
    echo [LOG] Проверьте logs\hintsage.log для деталей
    pause
)

echo.
echo [BYE] Hintsage завершен
pause


