# ====================================================
# Custom Docker Shutdown & Cleanup Script (PowerShell)
# ====================================================

Set-Location "$PSScriptRoot/.."

Write-Host "[1/3] Stopping Docker Compose services..."
docker compose down

Write-Host "`n[2/3] Removing Database file..."
$dbPath = "backend\app\database.db"

if (Test-Path $dbPath) {
    Remove-Item -Path $dbPath -Force
    Write-Host "    - Deleted $dbPath"
} else {
    Write-Host "    - Database file not found (already clean)"
}

Write-Host "`n[3/3] Removing Screenshots from backend folder..."
$pngPath = "backend\*.png"

if (Test-Path $pngPath) {
    Remove-Item -Path $pngPath -Force
    Write-Host "    - Deleted all .png screenshots"
} else {
    Write-Host "    - No screenshots found"
}

Write-Host "`n===================================================="
Write-Host "                 CLEANUP COMPLETE"
Write-Host "===================================================="