#!/bin/bash
# Media Empire Health Check Script
# Quickly see what's configured and what's broken

echo "=== MEDIA EMPIRE STATUS CHECK ==="
echo "Time: $(date)"
echo ""

# Check containers
echo "📦 CONTAINER STATUS:"
docker ps --format "  {{.Names}}: {{.Status}}" | sort
echo ""

# Check key configurations via API
echo "🔗 INTEGRATION STATUS:"

# Prowlarr apps
PROWLARR_APPS=$(curl -s "http://localhost:9696/api/v1/applications" -H "X-Api-Key: 1924e5254ee241bb9583a68ae1162864" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(', '.join([a['name'] for a in d]) if d else 'None')" 2>/dev/null || echo "ERROR")
echo "  Prowlarr → Apps: ${PROWLARR_APPS}"

# Radarr download clients
RADARR_DL=$(curl -s "http://localhost:7878/api/v3/downloadclient" -H "X-Api-Key: 4df9b2c5d0c641808fb9bd8e2d30c156" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(', '.join([c['name'] for c in d]) if d else 'None')" 2>/dev/null || echo "ERROR")
echo "  Radarr → Download Clients: ${RADARR_DL}"

# Sonarr download clients  
SONARR_DL=$(curl -s "http://localhost:8989/api/v3/downloadclient" -H "X-Api-Key: 3b2b941b68bc40aa822ee14d58f28786" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(', '.join([c['name'] for c in d]) if d else 'None')" 2>/dev/null || echo "ERROR")
echo "  Sonarr → Download Clients: ${SONARR_DL}"

# Jellyseerr init status
JELLYSEERR_INIT=$(cat /home/ryan/media-empire-1/config/jellyseerr/settings.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅ Complete' if d.get('public',{}).get('initialized') else '❌ Not completed')" 2>/dev/null || echo "ERROR")
echo "  Jellyseerr Setup: ${JELLYSEERR_INIT}"

# Bazarr config
BAZARR_RADARR=$(grep -A2 "^radarr:" /home/ryan/media-empire-1/config/bazarr/config/config.yaml 2>/dev/null | grep "ip:" | grep -v "127.0.0.1" && echo "✅" || echo "❌")
echo "  Bazarr → Radarr: ${BAZARR_RADARR}"

BAZARR_SONARR=$(grep -A2 "^sonarr:" /home/ryan/media-empire-1/config/bazarr/config/config.yaml 2>/dev/null | grep "ip:" | grep -v "127.0.0.1" && echo "✅" || echo "❌")
echo "  Bazarr → Sonarr: ${BAZARR_SONARR}"

echo ""
echo "📁 BACKUP STATUS:"
ls -lht /home/ryan/media-empire-1/backups/config_backup_*.tar.gz 2>/dev/null | head -3 || echo "  ⚠️  No backups found! Run: ./scripts/backup-configs.sh"

echo ""
echo "=== END STATUS ==="
