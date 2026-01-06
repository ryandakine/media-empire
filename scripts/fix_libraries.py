import requests
import json
import time

BASE_URL = "http://localhost:8096"
HEADERS = {}

def authenticate():
    global HEADERS
    url = f"{BASE_URL}/Users/AuthenticateByName"
    headers = {
        "Content-Type": "application/json",
        "X-Emby-Authorization": 'MediaBrowser Client="SetupScript", Device="Terminal", DeviceId="setup123", Version="1.0.0"'
    }
    payload = {"Username": "ryan", "Pw": "password123"}
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == 200:
        data = r.json()
        HEADERS = {"X-Emby-Token": data['AccessToken'], "Content-Type": "application/json"}
        return True
    return False

def recreate_library(name, path, content_type):
    print(f"🔧 Recreating Library: {name}")
    
    # 1. Delete if exists
    r = requests.get(f"{BASE_URL}/Library/VirtualFolders", headers=HEADERS)
    folders = r.json()
    target = next((f for f in folders if f['Name'] == name), None)
    
    if target:
        print(f"   🗑️ Deleting empty/broken library '{name}'...")
        # Delete param 'name' (query param) implies the folder name
        r_del = requests.delete(f"{BASE_URL}/Library/VirtualFolders", params={"Name": name}, headers=HEADERS)
        if r_del.status_code != 200 and r_del.status_code != 204:
             print(f"   ❌ Failed to delete: {r_del.status_code}")
             return
        time.sleep(1)

    # 2. Create New with Path
    print(f"   ✨ Creating '{name}' with path '{path}'...")
    
    # Using LibraryOptions in the body for initial creation is the most robust way in 10.8+
    payload = {
        "Name": name,
        "CollectionType": content_type,
        "LibraryOptions": {
            "PathInfos": [{"Path": path}],
            "EnableRealtimeMonitor": True
        }
    }
    
    # Some versions demand query params for Name/CollectionType AND body
    r = requests.post(f"{BASE_URL}/Library/VirtualFolders", params={
        "Name": name,
        "CollectionType": content_type
    }, json=payload, headers=HEADERS)
    
    if r.status_code == 200:
        print("   ✅ Created successfully.")
    else:
        print(f"   ❌ Creation failed: {r.text}")

authenticate()
recreate_library("Movies", "/media/movies", "movies")
recreate_library("TV Shows", "/media/tv", "tvshows")
requests.post(f"{BASE_URL}/Library/Refresh", headers=HEADERS)
print("🔄 Scan triggered.")
