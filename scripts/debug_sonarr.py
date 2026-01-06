import requests
import json

SONARR_URL = "http://localhost:8989/api/v3"
SONARR_KEY = "3b2b941b68bc40aa822ee14d58f28786"

def check_sonarr_history():
    print("📜 Checking Sonarr History...")
    r = requests.get(f"{SONARR_URL}/history", headers={"X-Api-Key": SONARR_KEY})
    history = r.json().get('records', [])
    
    if not history:
        print("   (No history found)")
        return
        
    for h in history[:5]:
         print(f"   - {h['eventType']}: {h['sourceTitle']} ({h.get('data', {}).get('reason', '')})")

if __name__ == "__main__":
    check_sonarr_history()
