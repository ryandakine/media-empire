# Media Empire

A self-hosted media server stack using Docker Compose.

## Services Included

- **Jellyfin** - Media streaming server (port 8096)
- **Radarr** - Movie management (port 7878)
- **Sonarr** - TV show management (port 8989)
- **Prowlarr** - Indexer manager (port 9696)
- **SABnzbd** - Usenet downloader (port 8085)
- **qBittorrent** - Torrent client (port 8080)
- **RDT-Client** - Real-Debrid integration (port 6500)
- **Jellyseerr** - Request management (port 5055)
- **Bazarr** - Subtitles (port 6767)
- **Tautulli** - Analytics (port 8181)
- **Tdarr** - Transcoding (port 8265)
- **Nginx Proxy Manager** - Reverse proxy (port 81)

## Quick Start

1. Clone this repo
2. Create necessary directories:
   ```bash
   mkdir -p config downloads media/{movies,tv,usenet}
   ```
3. Start the stack:
   ```bash
   docker compose up -d
   ```

## Configuration

- All configs are stored in `./config/`
- Media is stored in `./media/` (or your external drive)
- Downloads go to `./downloads/`

## Default Ports

| Service | Port |
|---------|------|
| Jellyfin | 8096 |
| Radarr | 7878 |
| Sonarr | 8989 |
| Prowlarr | 9696 |
| SABnzbd | 8085 |
| Jellyseerr | 5055 |

## License

MIT
