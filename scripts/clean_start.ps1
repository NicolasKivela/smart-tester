# ====================================================
# Custom Docker Compose Up & Cleanup Script (PowerShell)
# ====================================================

Set-Location "$PSScriptRoot/.."

Write-Host "[1/4] Stopping Docker Compose services..."
docker compose down

Write-Host "`n[2/4] Removing Database file..."
$dbPath = "backend\app\database.db"

if (Test-Path $dbPath) {
    Remove-Item -Path $dbPath -Force
    Write-Host "    - Deleted $dbPath"
} else {
    Write-Host "    - Database file not found (already clean)"
}

Write-Host "`n[3/4] Removing Screenshots from backend folder..."
$pngPath = "backend\*.png"

if (Test-Path $pngPath) {
    Remove-Item -Path $pngPath -Force
    Write-Host "    - Deleted all .png screenshots"
} else {
    Write-Host "    - No screenshots found"
}

Write-Host "`n[4/4] Starting Docker Compose services..."
docker compose up --build