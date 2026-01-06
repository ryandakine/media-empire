import requests
import json
import random
import time

# Configuration
RADARR_URL = "http://localhost:7878/api/v3"
RADARR_KEY = "4df9b2c5d0c641808fb9bd8e2d30c156"
SONARR_URL = "http://localhost:8989/api/v3"
SONARR_KEY = "3b2b941b68bc40aa822ee14d58f28786"

def add_movie(title):
    print(f"🎬 Searching for movie: {title}...")
    # Lookup
    r = requests.get(f"{RADARR_URL}/movie/lookup", params={"term": title}, headers={"X-Api-Key": RADARR_KEY})
    if r.status_code != 200:
        print(f"❌ Failed to lookup movie: {r.text}")
        return
    
    movies = r.json()
    if not movies:
        print("❌ Movie not found")
        return
        
    movie = movies[0]
    print(f"✅ Found: {movie['title']} ({movie['year']})")
    
    # Check if already exists
    if 'id' in movie and movie['id'] > 0:
        print("ℹ️ Movie already exists in Radarr")
        return

    # Add parameters
    payload = {
        "title": movie['title'],
        "qualityProfileId": 1, # Default
        "titleSlug": movie['titleSlug'],
        "images": movie['images'],
        "tmdbId": movie['tmdbId'],
        "year": movie['year'],
        "rootFolderPath": "/movies",
        "monitored": True,
        "addOptions": {
            "searchForMovie": True
        }
    }
    
    print("📥 Adding and searching for movie...")
    r = requests.post(f"{RADARR_URL}/movie", json=payload, headers={"X-Api-Key": RADARR_KEY})
    if r.status_code == 201:
        print(f"✅ Successfully added '{movie['title']}' to download queue")
    else:
        print(f"❌ Failed to add movie: {r.text}")

def add_show(title, seasons_to_download=[1, 10]):
    print(f"\n📺 Searching for show: {title}...")
    # Lookup
    r = requests.get(f"{SONARR_URL}/series/lookup", params={"term": title}, headers={"X-Api-Key": SONARR_KEY})
    if r.status_code != 200:
        print(f"❌ Failed to lookup show: {r.text}")
        return

    shows = r.json()
    if not shows:
        print("❌ Show not found")
        return
    
    show = shows[0]
    print(f"✅ Found: {show['title']}")

    # Prepare season monitoring
    # We want to Monitor ONLY the specific seasons requested to save bandwidth/checks
    # But for simplicity, we first add the show, then we can trigger a search.
    # Actually, Sonarr allows setting `monitored` per season in the add payload.
    
    seasons_payload = []
    for season in show['seasons']:
        is_wanted = season['seasonNumber'] in seasons_to_download
        season['monitored'] = is_wanted
        seasons_payload.append(season)
        if is_wanted:
             print(f"   - Marked Season {season['seasonNumber']} for download")

    payload = {
        "title": show['title'],
        "qualityProfileId": 1, # Default
        "titleSlug": show['titleSlug'],
        "images": show['images'],
        "tvdbId": show['tvdbId'],
        "seasons": seasons_payload,
        "rootFolderPath": "/tv",
        "monitored": True,
        "addOptions": {
            "searchForMissingEpisodes": True
        }
    }
    
    print(f"📥 Adding '{show['title']}' and searching for Seasons {seasons_to_download}...")
    r = requests.post(f"{SONARR_URL}/series", json=payload, headers={"X-Api-Key": SONARR_KEY})
    
    if r.status_code == 201:
        print(f"✅ Successfully added '{show['title']}' to download queue")
    elif r.status_code == 400 and "already" in r.text.lower():
         print("ℹ️ Show already exists. Triggering search manually...")
         # Get existing series ID
         r_exist = requests.get(f"{SONARR_URL}/series", headers={"X-Api-Key": SONARR_KEY})
         existing = [s for s in r_exist.json() if s['tvdbId'] == show['tvdbId']][0]
         
         # Trigger Season Search
         search_payload = {
             "name": "SeasonSearch",
             "seriesId": existing['id'],
             "seasonNumber": seasons_to_download[0] # Just search one for now to prove it
         }
         requests.post(f"{SONARR_URL}/command", json=search_payload, headers={"X-Api-Key": SONARR_KEY})
         print("✅ Search triggered for existing show")
    else:
        print(f"❌ Failed to add show: {r.text}")

if __name__ == "__main__":
    add_movie("The Big Lebowski")
    add_show("South Park", seasons_to_download=[1, 10])
