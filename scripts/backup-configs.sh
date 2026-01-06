#!/bin/bash
# Media Empire Config Backup Script
# Run this AFTER completing any setup to preserve your configurations

BACKUP_DIR="/home/ryan/media-empire-1/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="config_backup_${TIMESTAMP}"

echo "=== Media Empire Config Backup ==="
echo "Creating backup: ${BACKUP_NAME}"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Create tarball of entire config directory
tar -czvf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" -C /home/ryan/media-empire-1 config/

echo ""
echo "✅ Backup created: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo ""

# Keep only last 5 backups
echo "Cleaning old backups (keeping last 5)..."
ls -t "${BACKUP_DIR}"/config_backup_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm -f

echo "Current backups:"
ls -lh "${BACKUP_DIR}"/config_backup_*.tar.gz 2>/dev/null || echo "No backups found"
