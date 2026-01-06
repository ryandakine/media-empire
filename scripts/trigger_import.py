import requests
import json
import time

RADARR_URL = "http://localhost:7878/api/v3"
RADARR_KEY = "4df9b2c5d0c641808fb9bd8e2d30c156"

# Command: Downloaded Movies Scan
# This tells Radarr: "Check your download client path (now valid) and import files"
def text_radarr_import():
    print("🚀 Triggering 'DownloadedMoviesScan'...")
    payload = {
        "name": "DownloadedMoviesScan",
        "path": "/downloads"  # Force check this path
    }
    
    try:
        r = requests.post(f"{RADARR_URL}/command", json=payload, headers={"X-Api-Key": RADARR_KEY})
        if r.status_code == 201:
            print("✅ Scan triggered successfully.")
            data = r.json()
            print(f"   Command ID: {data['id']}")
            print(f"   Status: {data['status']}")
            
            # Monitor
            print("⏳ Monitoring status...")
            cmd_id = data['id']
            for _ in range(10): # Wait up to 20s
                time.sleep(2)
                r_stat = requests.get(f"{RADARR_URL}/command/{cmd_id}", headers={"X-Api-Key": RADARR_KEY})
                if r_stat.status_code == 200:
                    stat = r_stat.json()
                    print(f"   Status: {stat['status']}")
                    if stat['status'] == 'completed':
                        print("✅ Scan completed.")
                        break
        else:
             print(f"❌ Failed to trigger scan: {r.text}")
             
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    text_radarr_import()
