#!/bin/bash
# Media Empire Config Restore Script
# Use this to restore configurations after an accidental reset

BACKUP_DIR="/home/ryan/media-empire-1/backups"

echo "=== Media Empire Config Restore ==="
echo ""

# List available backups
echo "Available backups:"
ls -lht "${BACKUP_DIR}"/config_backup_*.tar.gz 2>/dev/null
echo ""

if [ -z "$1" ]; then
    # Use most recent backup if no argument provided
    BACKUP_FILE=$(ls -t "${BACKUP_DIR}"/config_backup_*.tar.gz 2>/dev/null | head -1)
    if [ -z "$BACKUP_FILE" ]; then
        echo "❌ No backup files found in ${BACKUP_DIR}"
        exit 1
    fi
    echo "Using most recent backup: ${BACKUP_FILE}"
else
    BACKUP_FILE="$1"
fi

echo ""
read -p "⚠️  This will overwrite current configs. Continue? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Stopping containers..."
cd /home/ryan/media-empire-1
docker-compose stop

echo ""
echo "Restoring from backup..."
tar -xzvf "${BACKUP_FILE}" -C /home/ryan/media-empire-1

echo ""
echo "Starting containers..."
docker-compose start

echo ""
echo "✅ Restore complete!"
echo ""
echo "Note: You may need to wait a minute for services to fully start."
