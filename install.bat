@echo off
REM Скрипт автоматической установки Hintsage для Windows

echo ============================================
echo      Hintsage - AI Interview Assistant
echo           Автоматическая установка
echo ============================================
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден!
    echo Установите Python 3.10+ с https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Создание виртуального окружения
echo [2/5] Создание виртуального окружения...
if exist venv (
    echo Виртуальное окружение уже существует
) else (
    python -m venv venv
    echo Виртуальное окружение создано
)
echo.

REM Активация окружения и установка зависимостей
echo [3/5] Установка зависимостей...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Копирование конфигурации
echo [4/5] Настройка конфигурации...
if exist config.yaml (
    echo config.yaml уже существует, пропускаем
) else (
    copy config.example.yaml config.yaml
    echo config.yaml создан из примера
    echo.
    echo ВАЖНО: Откройте config.yaml и добавьте ваш OpenAI API ключ!
)
echo.

REM Создание директорий
echo [5/5] Создание директорий...
if not exist data mkdir data
if not exist data\sessions mkdir data\sessions
if not exist data\screenshots mkdir data\screenshots
if not exist logs mkdir logs
if not exist models mkdir models
echo Директории созданы
echo.

echo ============================================
echo           Установка завершена!
echo ============================================
echo.
echo Следующие шаги:
echo.
echo 1. Скачайте Vosk модель (150 MB):
echo    https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
echo.
echo 2. Распакуйте в папку models\
echo.
echo 3. Откройте config.yaml и добавьте OpenAI API ключ:
echo    notepad config.yaml
echo.
echo 4. Запустите приложение:
echo    venv\Scripts\activate
echo    python main.py
echo.
echo Для тестирования модулей:
echo    python test_modules.py
echo.
pause


