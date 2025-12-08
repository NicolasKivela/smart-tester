@echo off
REM ====================================================
REM Custom Docker Compose Up & Cleanup Script
REM ====================================================

cd /d "%~dp0.."

echo [1/4] Stopping Docker Compose services...
docker compose down

echo.
echo [2/4] Removing Database file...
REM Check if the file exists on the HOST system before trying to delete it
if exist "backend\app\database.db" (
    del /F /Q "backend\app\database.db"
    echo    - Deleted backend\app\database.db
) else (
    echo    - Database file not found (already clean)
)

echo.
echo [3/4] Removing Screenshots from backend folder...
REM This removes all PNG files in the backend folder
if exist "backend\*.png" (
    del /F /Q "backend\*.png"
    echo    - Deleted all .png screenshots
) else (
    echo    - No screenshots found
)

echo [4/4] Starting Docker Compose services...
docker compose up --build