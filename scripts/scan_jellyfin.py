import requests
import json

BASE_URL = "http://localhost:8096"

def trigger_scan():
    print("🔄 Triggering Jellyfin Library Scan...")
    
    # Auth
    url = f"{BASE_URL}/Users/AuthenticateByName"
    headers = {
        "Content-Type": "application/json",
        "X-Emby-Authorization": 'MediaBrowser Client="SetupScript", Device="Terminal", DeviceId="setup123", Version="1.0.0"'
    }
    payload = {"Username": "ryan", "Pw": "password123"}
    r = requests.post(url, json=payload, headers=headers)
    
    if r.status_code == 200:
        token = r.json()['AccessToken']
        headers = {"X-Emby-Token": token}
        
        # Trigger Scan
        r = requests.post(f"{BASE_URL}/Library/Refresh", headers=headers)
        if r.status_code == 204:
            print("✅ Scan triggered successfully.")
        else:
            print(f"❌ Failed trigger: {r.status_code}")
            
    else:
        print("❌ Auth failed.")

if __name__ == "__main__":
    trigger_scan()
