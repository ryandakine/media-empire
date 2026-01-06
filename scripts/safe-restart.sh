#!/bin/bash
# Media Empire Safe Restart Script
# Use this instead of docker-compose down/up to prevent config loss

echo "=== Media Empire Safe Restart ==="
echo ""

cd /home/ryan/media-empire-1

# First, create a backup
echo "Creating backup before restart..."
./scripts/backup-configs.sh

echo ""
echo "Restarting containers (NOT recreating)..."
# Use 'restart' which preserves containers, NOT 'down && up'
docker-compose restart

echo ""
echo "✅ Safe restart complete!"
echo ""
echo "Container status:"
docker-compose ps
