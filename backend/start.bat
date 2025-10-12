@echo off
echo ========================================
echo   Hintsage Backend API
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo Swagger UI: http://localhost:8000/docs
echo.

uvicorn app.main:app --reload --port 8000

