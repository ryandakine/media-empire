import requests
import json

JELLYFIN_URL = "http://localhost:8096"
API_KEY = "675e2764dcce4cdd895c965cc6c6819b" # Using the one we saw in config
HEADERS = {
    "X-Emby-Token": API_KEY,
    "Content-Type": "application/json"
}

def add_library(name, path, content_type):
    print(f"Adding library: {name}...")
    
    # 1. Get Library Options
    payload = {
        "Name": name,
        "Path": path,
        "ContentType": content_type,
        "CollectionType": content_type,
        "LibraryOptions": {
            "EnablePhotos": False,
            "EnableRealtimeMonitor": True,
            "ExtractChapterImages": True,
            "ExtractChapterImagesDuringLibraryScan": True,
            "PathInfos": [{"Path": path}]
        }
    }
    
    # Jellyfin API for adding libraries is tricky, often easier to use /Library/VirtualFolders
    # Let's try to add the media path directly
    
    r = requests.post(f"{JELLYFIN_URL}/Library/VirtualFolders", params={
        "Name": name,
        "CollectionType": content_type,
        "RefreshLibrary": True
    }, headers=HEADERS)
    
    if r.status_code == 200:
        print(f"✅ Created Virtual Folder: {name}")
        
        # Now add the path to it
        r = requests.post(f"{JELLYFIN_URL}/Library/VirtualFolders/Paths", params={
            "Name": name,
            "Path": path,
            "RefreshLibrary": True
        }, headers=HEADERS)
        
        if r.status_code == 200:
             print(f"✅ Linked path {path} to {name}")
        else:
             print(f"❌ Failed to link path: {r.text}")
    else:
        print(f"❌ Failed to create library: {r.text}")

# Add Movies
add_library("Movies", "/movies", "movies")

# Add TV Shows
add_library("TV Shows", "/tv", "tvshows")

# Trigger Scan
print("Triggering Library Scan...")
requests.post(f"{JELLYFIN_URL}/Library/Refresh", headers=HEADERS)
print("✅ Configuration complete")
