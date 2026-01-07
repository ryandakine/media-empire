import requests
import json

RADARR_API_KEY = "4df9b2c5d0c641808fb9bd8e2d30c156"
RADARR_URL = "http://localhost:7878/api/v3"

def fix_remote_path_mappings():
    # 1. Get Host (SABnzbd)
    # We need to know what 'Host' Radarr thinks SABnzbd is. 
    # Usually it's the hostname 'sabnzbd' or the IP.
    
    # 2. Add Mapping
    payload = {
        "host": "sabnzbd",
        "remotePath": "/downloads/",
        "localPath": "/downloads/usenet/"
    }
    
    response = requests.post(
        f"{RADARR_URL}/remotepathmapping",
        headers={"X-Api-Key": RADARR_API_KEY, "Content-Type": "application/json"},
        json=payload
    )
    
    if response.status_code == 201:
        print("✅ Success! Remote Path Mapping added.")
        print(f"  Mapped '/downloads/' (SABnzbd) -> '/downloads/usenet/' (Radarr)")
        return True
    elif "exists" in response.text.lower():
         print("⚠️ Mapping already exists.")
         return True
    else:
        print(f"❌ Failed to add mapping: {response.status_code}")
        print(response.text)
        return False

def trigger_scan():
    print("🔄 Triggering 'Downloaded Movies Scan' to pick up files...")
    cmd_payload = {"name": "DownloadedMoviesScan"}
    requests.post(
        f"{RADARR_URL}/command",
        headers={"X-Api-Key": RADARR_API_KEY, "Content-Type": "application/json"},
        json=cmd_payload
    )

if __name__ == "__main__":
    if fix_remote_path_mappings():
        trigger_scan()
