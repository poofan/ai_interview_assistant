@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           Тестирование Hintsage.exe                        ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo ⏰ Запускаем Hintsage.exe...
echo    (приложение откроется в фоновом режиме)
echo.
echo ⚠️  Для остановки нажмите Ctrl+C
echo.

cd dist
start "" Hintsage.exe

echo.
echo ✅ Hintsage.exe запущен!
echo.
echo 📋 Проверьте:
echo    1. Открылось ли окно overlay
echo    2. Нет ли ошибок в консоли
echo    3. Работает ли триггер (Ctrl+Shift+Q)
echo.
pause

