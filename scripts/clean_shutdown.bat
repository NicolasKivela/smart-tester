@echo off
REM ====================================================
REM Custom Docker Shutdown & Cleanup Script
REM ====================================================

cd /d "%~dp0.."

echo [1/3] Stopping Docker Compose services...
docker compose down

echo.
echo [2/3] Removing Database file...
REM Check if the file exists on the HOST system before trying to delete it
if exist "backend\app\database.db" (
    del /F /Q "backend\app\database.db"
    echo    - Deleted backend\app\database.db
) else (
    echo    - Database file not found (already clean)
)

echo.
echo [3/3] Removing Screenshots from backend folder...
REM This removes all PNG files in the backend folder
if exist "backend\*.png" (
    del /F /Q "backend\*.png"
    echo    - Deleted all .png screenshots
) else (
    echo    - No screenshots found
)

echo.
echo ====================================================
echo                 CLEANUP COMPLETE
echo ====================================================