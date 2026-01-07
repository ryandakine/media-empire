# Media Empire Audit & Fixes - 2026-01-07

## Summary of Changes

This document details the critical fixes applied to stabilize your Media Empire stack. All changes have been committed to the repository.

---

## ✅ Issues Fixed

### 1. **CRITICAL: Missing .env File (Permission Issues)**
**Problem:** No `.env` file existed, causing all containers to run as root (PUID=0, PGID=0)
**Impact:** File permission issues, inability for apps to read/write downloads
**Fix Applied:** Created `.env` file with proper user/group configuration

**Action Required:**
```bash
cd /home/ryan/media-empire-1
# Verify/update these values to match your user:
id  # Check your actual PUID/PGID

# Edit .env and set correct values:
nano .env
# Update PUID and PGID if needed
# Update TZ to your timezone
```

---

### 2. **CRITICAL: qBittorrent Path Mismatch**
**Problem:** qBittorrent used `/downloads/torrents` while Radarr/Sonarr expected `/downloads`
**Impact:** Import failures, no hardlinking, duplicate files
**Fix Applied:** Changed qBittorrent volume mapping to match other services

**docker-compose.yml:30**
```yaml
# BEFORE:
- /media/ryan/ROOTFS/media_empire/downloads/torrents:/downloads

# AFTER:
- /media/ryan/ROOTFS/media_empire/downloads:/downloads
```

**Action Required After Restart:**
- Any existing torrents in the old `/downloads/torrents` folder will need to be moved or re-added

---

### 3. **CRITICAL: Hardcoded API Keys Exposed**
**Problem:** Radarr and Sonarr API keys were hardcoded in docker-compose.yml
**Impact:** Security vulnerability - anyone with repo access can control your services
**Fix Applied:** Moved API keys to environment variables

**docker-compose.yml:205-208**
```yaml
# BEFORE:
- UN_RADARR_0_API_KEY=4df9b2c5d0c641808fb9bd8e2d30c156
- UN_SONARR_0_API_KEY=3b2b941b68bc40aa822ee14d58f28786

# AFTER:
- UN_RADARR_0_API_KEY=${RADARR_API_KEY}
- UN_SONARR_0_API_KEY=${SONARR_API_KEY}
```

**Action Required:**
```bash
# 1. Regenerate API keys (the old ones are compromised):
#    - Radarr: Settings > General > Security > API Key > Regenerate
#    - Sonarr: Settings > General > Security > API Key > Regenerate

# 2. Add new keys to .env:
nano .env
# Add:
# RADARR_API_KEY=your_new_key_here
# SONARR_API_KEY=your_new_key_here
```

---

### 4. **NEW: Cloudflare Tunnel Service Added**
**Problem:** No cloudflared service in docker-compose.yml
**Impact:** External access may have been unstable or manually managed
**Fix Applied:** Added cloudflared service to docker-compose.yml

**Action Required:**
```bash
# Get your tunnel token from Cloudflare:
# 1. Go to: https://dash.cloudflare.com/
# 2. Navigate: Zero Trust > Access > Tunnels
# 3. Select your tunnel (or create new one)
# 4. Copy the tunnel token

# Add to .env:
nano .env
# Add:
# CLOUDFLARE_TUNNEL_TOKEN=your_token_here
```

**Note:** If you're already running cloudflared separately, you can comment out this service or stop your existing instance.

---

### 5. **SECURITY: Ports Secured to Localhost**
**Problem:** All services were exposed to 0.0.0.0 (all network interfaces)
**Impact:** If your server has a public IP, services were accessible from internet
**Fix Applied:** Bound all management ports to 127.0.0.1 (localhost only)

**Services Secured:**
- SABnzbd: `127.0.0.1:8085`
- qBittorrent: `127.0.0.1:8082`
- Prowlarr: `127.0.0.1:9696`
- Radarr: `127.0.0.1:7878`
- Sonarr: `127.0.0.1:8989`
- Jellyseerr: `127.0.0.1:5055`
- RDT-Client: `127.0.0.1:6500`
- Bazarr: `127.0.0.1:6767`
- Tautulli: `127.0.0.1:8181`
- Tdarr: `127.0.0.1:8265, 127.0.0.1:8266`

**Services Left Public (intentional):**
- Jellyfin: `8096` (media streaming)
- Nginx Proxy Manager: `80, 81, 443` (reverse proxy)

**Impact:** You must now access these services via:
- Localhost: `http://localhost:8085`
- Cloudflare Tunnel: `https://media.osi-cyber.com` (if configured)
- SSH Tunnel: `ssh -L 8085:localhost:8085 user@server`

---

## 🚀 Deployment Instructions

### Step 1: Verify Your Environment
```bash
cd /home/ryan/media-empire-1

# Pull latest changes:
git pull origin claude/debug-media-empire-mYRkL

# Verify .env exists:
ls -la .env

# Check your user ID (should match .env):
id
```

### Step 2: Configure .env File
```bash
nano .env

# Required values:
PUID=1000              # Set to your user ID
PGID=1000              # Set to your group ID
TZ=America/Los_Angeles # Set to your timezone

# CRITICAL - Regenerate these (old ones are compromised):
RADARR_API_KEY=get_from_radarr_settings
SONARR_API_KEY=get_from_sonarr_settings

# Optional - for Cloudflare tunnel:
CLOUDFLARE_TUNNEL_TOKEN=get_from_cloudflare_dashboard
```

### Step 3: Stop Existing Stack
```bash
docker compose down
```

### Step 4: Restart with New Configuration
```bash
docker compose up -d

# Watch logs for any errors:
docker compose logs -f
```

### Step 5: Verify Services
```bash
# Check all containers are running:
docker compose ps

# Test localhost access:
curl -I http://localhost:8096/health  # Jellyfin
curl -I http://localhost:8085         # SABnzbd
curl -I http://localhost:7878         # Radarr
curl -I http://localhost:8989         # Sonarr
```

---

## 🔍 Post-Deployment Verification Checklist

### Volume Mappings
- [ ] All services use same `/downloads` path
- [ ] Check: `docker compose config | grep downloads`
- [ ] Verify no more `/downloads/torrents` references

### Permissions
- [ ] Downloaded files have correct ownership
- [ ] Check: `ls -la /media/ryan/ROOTFS/media_empire/downloads/`
- [ ] Owner should be your user, not root

### API Connectivity
- [ ] Radarr can communicate with SABnzbd
- [ ] Sonarr can communicate with SABnzbd
- [ ] Prowlarr is synced with Radarr/Sonarr
- [ ] Unpackerr is monitoring Radarr/Sonarr queues

### Network Access
- [ ] Jellyfin accessible at `http://localhost:8096`
- [ ] Cloudflare tunnel working (if configured)
- [ ] SSH tunneling works if needed
- [ ] Services NOT accessible from public IP directly

### End-to-End Test
- [ ] Add a test movie in Radarr
- [ ] Verify it appears in SABnzbd queue
- [ ] Watch it download and import
- [ ] Confirm movie appears in Jellyfin
- [ ] Verify hardlinking worked (no duplicate files)

---

## ⚠️ Known Limitations

### Cannot Verify Without Live Access:
- SABnzbd download speeds (need to check in UI)
- Actual network interface priority (WiFi vs Ethernet)
- SABnzbd `direct_unpack` setting (check `/config/sabnzbd/sabnzbd.ini`)
- Cloudflare tunnel logs (check `docker compose logs cloudflared`)
- Existing download queue status

### Manual Checks Required:
1. **SABnzbd Speed Test:**
   - Open SABnzbd UI: `http://localhost:8085`
   - Start a download
   - Verify speed is >20 MB/s

2. **Network Priority:**
   ```bash
   ip route show | grep default
   # Ethernet (enx...) should have lower metric than WiFi (wlp...)
   ```

3. **SABnzbd Config:**
   ```bash
   grep "direct_unpack" /home/ryan/media-empire-1/config/sabnzbd/sabnzbd.ini
   # Should be: direct_unpack = 0 (disabled for speed)
   ```

---

## 📝 Additional Recommendations

### 1. Add External Drive Mount Check
Create a systemd check to ensure `/media/ryan/ROOTFS/` is mounted before starting Docker.

### 2. Consider Moving to Docker Secrets
For production, consider using Docker Swarm secrets instead of .env file.

### 3. Regular API Key Rotation
Schedule quarterly API key regeneration for security.

### 4. Backup Configuration
```bash
# Backup your configs regularly:
tar -czf media-empire-backup-$(date +%Y%m%d).tar.gz \
  /home/ryan/media-empire-1/config \
  /home/ryan/media-empire-1/.env \
  /home/ryan/media-empire-1/docker-compose.yml
```

### 5. Monitor Disk Space
```bash
# Add to cron to monitor external drive:
df -h /media/ryan/ROOTFS/media_empire/ | tail -1 | awk '{print $5}' | sed 's/%//'
# Alert if >90%
```

---

## 🐛 Troubleshooting Common Issues

### Issue: "Permission Denied" errors
**Solution:** Verify PUID/PGID in .env matches your user
```bash
id
# Update .env with correct values
docker compose down && docker compose up -d
```

### Issue: Import failures in Radarr/Sonarr
**Solution:** Check path mappings
```bash
docker exec radarr ls -la /downloads
docker exec sonarr ls -la /downloads
# Both should show same files
```

### Issue: Can't access services remotely
**Solution:** Ports are now localhost-only. Use:
- Cloudflare Tunnel (configure in .env)
- SSH Tunnel: `ssh -L 8085:localhost:8085 ryan@server-ip`
- Or revert specific ports to 0.0.0.0 if needed

### Issue: Unpackerr not working
**Solution:** Regenerate and add API keys to .env
```bash
# Get new keys from Radarr/Sonarr settings
nano .env
# Add RADARR_API_KEY and SONARR_API_KEY
docker compose restart unpackerr
```

### Issue: Cloudflared failing to start
**Solution:** Add tunnel token to .env
```bash
# Get token from Cloudflare dashboard
nano .env
# Add CLOUDFLARE_TUNNEL_TOKEN=...
docker compose restart cloudflared
```

---

## 📊 Root Causes of Your Instability

Based on the audit, your instability was caused by:

1. **Permission Issues (High Severity)**
   - Running as root instead of your user
   - Files created with wrong ownership
   - Apps unable to read/write properly

2. **Path Mismatches (High Severity)**
   - qBittorrent using different download path
   - Radarr/Sonarr couldn't find downloaded files
   - Import failures and duplicate files

3. **Security Exposure (Medium Severity)**
   - Hardcoded API keys allowed unauthorized access
   - All ports exposed to public internet

4. **Configuration Drift (Medium Severity)**
   - No Cloudflare tunnel management in Docker
   - Inconsistent service access patterns

---

## ✉️ Support

If you encounter issues after applying these fixes:
1. Check container logs: `docker compose logs [service-name]`
2. Verify .env values are correct
3. Ensure external drive is mounted
4. Review this document's troubleshooting section

---

**Generated:** 2026-01-07
**Stack Version:** Docker Compose v3
**Services:** 13 containers
**Changes:** 5 critical fixes applied
