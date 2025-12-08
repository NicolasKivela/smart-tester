#!/bin/bash
# ====================================================
# Custom Docker Shutdown & Cleanup Script (Bash)
# ====================================================

cd "$(dirname "$0")/.." || exit

echo "[1/3] Stopping Docker Compose services..."
docker compose down

echo ""
echo "[2/3] Removing Database file..."
DB_FILE="backend/app/database.db"

if [ -f "$DB_FILE" ]; then
    rm -f "$DB_FILE"
    echo "    - Deleted $DB_FILE"
else
    echo "    - Database file not found (already clean)"
fi

echo ""
echo "[3/3] Removing Screenshots from backend folder..."
# Check for png files before trying to remove to avoid "No such file" warnings
if ls backend/*.png 1> /dev/null 2>&1; then
    rm -f backend/*.png
    echo "    - Deleted all .png screenshots"
else
    echo "    - No screenshots found"
fi

echo ""
echo "===================================================="
echo "                 CLEANUP COMPLETE"
echo "===================================================="