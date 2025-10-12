@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║        Hintsage - Сборка EXE (PyInstaller)                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:: Активация виртуального окружения
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Ошибка: виртуальное окружение не найдено
    echo    Запустите сначала: install.bat
    pause
    exit /b 1
)

:: Установка PyInstaller если нет
echo [1/4] Проверка PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo    Installing PyInstaller...
    pip install pyinstaller
)

:: Очистка старых сборок
echo [2/4] Очистка старых сборок...
if exist "dist\Hintsage.exe" del /f /q "dist\Hintsage.exe"
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

:: Сборка
echo [3/4] Сборка приложения...
echo    ⏳ Это может занять 5-10 минут...
echo.
pyinstaller --clean hintsage.spec

:: Проверка результата
echo [4/4] Проверка результата...
if exist "dist\Hintsage.exe" (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                    ✅ УСПЕШНО!                             ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo 📦 Файл: dist\Hintsage.exe
    
    :: Размер файла
    for %%A in ("dist\Hintsage.exe") do (
        set size=%%~zA
        set /a sizeMB=!size! / 1048576
    )
    echo 📊 Размер: %sizeMB% MB
    echo.
    echo 🚀 Запуск:
    echo    1. Скопируйте dist\Hintsage.exe куда угодно
    echo    2. Запустите двойным кликом
    echo    3. Или используйте start_silent.vbs
    echo.
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                    ❌ ОШИБКА!                              ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Проверьте вывод выше для деталей
    echo.
)

pause

