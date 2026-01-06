import requests
import json
import time

RADARR_URL = "http://localhost:7878/api/v3"
RADARR_KEY = "4df9b2c5d0c641808fb9bd8e2d30c156"

def check_radarr_status():
    print("re: Checking Radarr Status...")
    
    # 1. Check Movies
    r = requests.get(f"{RADARR_URL}/movie", headers={"X-Api-Key": RADARR_KEY})
    movies = r.json()
    print(f"🎬 Movies in Radarr: {len(movies)}")
    for m in movies:
        print(f"   - {m['title']} (Monitored: {m['monitored']}, Status: {m['status']})")
    
    # 2. Check History (Failed grabs?)
    r = requests.get(f"{RADARR_URL}/history", headers={"X-Api-Key": RADARR_KEY})
    history = r.json().get('records', [])
    print(f"\n📜 Recent History ({len(history)} items):")
    for h in history[:5]:
         print(f"   - {h['eventType']}: {h['sourceTitle']} ({h.get('data', {}).get('reason', '')})")

    # 3. Check Indexers
    r = requests.get(f"{RADARR_URL}/indexer", headers={"X-Api-Key": RADARR_KEY})
    indexers = r.json()
    print(f"\n🔎 Indexers ({len(indexers)}):")
    for i in indexers:
        print(f"   - {i['name']} (Enabled: {i['enable']})")

if __name__ == "__main__":
    check_radarr_status()
