@echo off
REM Быстрый запуск Hintsage (без пауз)
chcp 65001 >nul
cd /d "%~dp0"
venv\Scripts\python.exe main.py


