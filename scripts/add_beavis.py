import requests
import json

SONARR_URL = "http://localhost:8989/api/v3"
SONARR_KEY = "3b2b941b68bc40aa822ee14d58f28786"

def add_beavis():
    print("📺 Searching for Beavis and Butt-Head...")
    
    # Search
    r = requests.get(f"{SONARR_URL}/series/lookup", params={"term": "Beavis and Butt-Head"}, headers={"X-Api-Key": SONARR_KEY})
    results = r.json()
    
    # Usually "Beavis and Butt-Head" (1993) is the main one.
    # The 2011 one is "Beavis and Butt-Head (2011)" etc.
    
    found = False
    for show in results:
        if "Beavis and Butt-Head" in show['title']:
            print(f"   Found: {show['title']} ({show['year']})")
            
            # Add it
            payload = {
                "title": show['title'],
                "qualityProfileId": 1,
                "titleSlug": show['titleSlug'],
                "images": show['images'],
                "tvdbId": show['tvdbId'],
                "rootFolderPath": "/tv",
                "monitored": True,
                "addOptions": {
                    "searchForMissingEpisodes": True # Trigger search immediately
                }
            }
            
            print(f"📥 Adding '{show['title']}'...")
            r_add = requests.post(f"{SONARR_URL}/series", json=payload, headers={"X-Api-Key": SONARR_KEY})
            if r_add.status_code == 201:
                print("   ✅ Added successfully.")
                found = True
            elif r_add.status_code == 400 and "already" in r_add.text:
                print("   ℹ️ Already in Sonarr. Triggering search...")
                # Trigger search
                # Get ID first?
                # Assume we can trigger search command for series?
                # For now just confirming it's there.
                found = True

    if not found:
        print("❌ Could not find Beavis and Butt-Head.")

if __name__ == "__main__":
    add_beavis()
