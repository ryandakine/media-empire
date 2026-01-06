import requests
import json

QB_URL = "http://localhost:8082"
USERNAME = "admin"
PASSWORD = "password123"

def get_torrents():
    s = requests.Session()
    
    # Login
    print("🔐 Logging into qBittorrent...")
    r = s.post(f"{QB_URL}/api/v2/auth/login", data={"username": USERNAME, "password": PASSWORD})
    if r.status_code != 200:
        print(f"❌ Login failed: {r.text}")
        return

    print("✅ Login successful")
    
    # Get Torrents
    print("📡 Fetching torrents...")
    r = s.get(f"{QB_URL}/api/v2/torrents/info")
    if r.status_code != 200:
         print(f"❌ Failed to get torrents: {r.text}")
         return
         
    torrents = r.json()
    if not torrents:
        print("ℹ️ No torrents found in qBittorrent.")
    else:
        print(f"✅ Found {len(torrents)} torrents:")
        for t in torrents:
            print(f"   - [{t['state']}] {t['name']} ({t['progress']*100:.1f}%)")

if __name__ == "__main__":
    get_torrents()
