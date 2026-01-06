import requests
import json

RADARR_URL = "http://localhost:7878/api/v3"
RADARR_KEY = "4df9b2c5d0c641808fb9bd8e2d30c156"

MOVIES = [
    "Tron",
    "Tron Legacy",
    "Mission Impossible",
    "Mission Impossible Dead Reckoning",
    "F1",
    "Snatch",
    "Troy",
    "Avatar",
    "Deadpool & Wolverine", 
    "Frankenstein",
    "Now You See Me"
]

def add_movies():
    print("🎬 Bulk Adding Movies to Radarr...")
    
    for term in MOVIES:
        try:
            # Search
            r = requests.get(f"{RADARR_URL}/movie/lookup", params={"term": term}, headers={"X-Api-Key": RADARR_KEY})
            results = r.json()
            
            if not results:
                print(f"❌ '{term}' not found.")
                continue
                
            # Pick first match usually
            movie = results[0]
            print(f"   Found: {movie['title']} ({movie['year']})")
            
            # Add
            payload = {
                "title": movie['title'],
                "qualityProfileId": 1, 
                "titleSlug": movie['titleSlug'],
                "images": movie['images'],
                "tmdbId": movie['tmdbId'],
                "rootFolderPath": "/movies",
                "monitored": True,
                "addOptions": {
                    "searchForMovie": True
                }
            }
            
            r_add = requests.post(f"{RADARR_URL}/movie", json=payload, headers={"X-Api-Key": RADARR_KEY})
            if r_add.status_code == 201:
                print("      ✅ Added & Searching.")
            elif r_add.status_code == 400 and "already" in r_add.text:
                print("      ℹ️ Already exists.")
                # Maybe trigger search if exists?
        except Exception as e:
            print(f"   ❌ Error searching {term}: {e}")

if __name__ == "__main__":
    add_movies()
