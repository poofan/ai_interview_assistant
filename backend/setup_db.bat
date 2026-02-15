@echo off
echo ========================================
echo   Hintsage Database Setup
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo Step 1: Checking PostgreSQL connection...
python -c "from app.database import engine; engine.connect(); print('✅ PostgreSQL connected!')" 2>nul
if errorlevel 1 (
    echo.
    echo ⚠️  PostgreSQL connection failed!
    echo.
    echo Please make sure:
    echo 1. PostgreSQL is installed and running
    echo 2. Database 'hintsage' exists
    echo 3. .env file has correct DATABASE_URL
    echo.
    echo To create database, run:
    echo   psql -U postgres -c "CREATE DATABASE hintsage;"
    echo.
    pause
    exit /b 1
)

echo.
echo Step 2: Running database migrations...
alembic upgrade head

if errorlevel 1 (
    echo.
    echo ❌ Migration failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ Database setup complete!
echo ========================================
echo.
echo Tables created:
echo   - users
echo   - subscriptions
echo   - payments
echo   - app_versions
echo.
echo You can now start the API server with:
echo   start.bat
echo.
pause

