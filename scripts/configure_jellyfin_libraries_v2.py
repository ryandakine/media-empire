import requests
import json

BASE_URL = "http://localhost:8096"

def get_auth_header():
    # Authenticate to get a real session token
    url = f"{BASE_URL}/Users/AuthenticateByName"
    headers = {
        "Content-Type": "application/json",
        "X-Emby-Authorization": 'MediaBrowser Client="SetupScript", Device="Terminal", DeviceId="setup123", Version="1.0.0"'
    }
    payload = {
        "Username": "ryan",
        "Pw": "password123"
    }
    
    print("🔐 Authenticating...")
    r = requests.post(url, json=payload, headers=headers)
    
    if r.status_code != 200:
        print(f"❌ Auth failed: {r.status_code} {r.text}")
        # Try admin/password123 as fallback
        payload["Username"] = "admin"
        r = requests.post(url, json=payload, headers=headers)
        if r.status_code != 200:
             print("❌ Admin auth also failed.")
             exit(1)
        print("✅ Authenticated as 'admin'")
    else:
        print("✅ Authenticated as 'ryan'")
        
    data = r.json()
    token = data['AccessToken']
    user_id = data['User']['Id']
    
    return {
        "X-Emby-Token": token,
        "Content-Type": "application/json"
    }

HEADERS = get_auth_header()

def add_library(name, path, content_type):
    print(f"📚 Adding library: {name}...")
    
    # Check if exists first
    r = requests.get(f"{BASE_URL}/Library/VirtualFolders", headers=HEADERS)
    existing = [l['Name'] for l in r.json()]
    if name in existing:
        print(f"   ℹ️ Library '{name}' already exists. Verifying path...")
    else:
        # Create Library
        # The API expects query params for the initial creation of the folder
        r = requests.post(f"{BASE_URL}/Library/VirtualFolders", params={
            "Name": name,
            "CollectionType": content_type,
            "RefreshLibrary": "false" # Don't scan yet
        }, headers=HEADERS)
        
        if r.status_code != 200:
             print(f"❌ Failed to create library folder: {r.text}")
             return
             
        print(f"   ✅ Library folder created.")

    # Now ADD the path to the library
    # We need to know the 'ItemId' potentially, usually handled by Name lookup internally or separate endpoint
    # The correct endpoint to ADD a path to a virtual folder is POST /Library/VirtualFolders/Paths
    path_payload = {
        "Name": name,
        "Path": path,
        "PathInfo": {
            "Path": path
        }
    }
    
    r = requests.post(f"{BASE_URL}/Library/VirtualFolders/Paths", params={
        "RefreshLibrary": "true"
    }, json=path_payload, headers=HEADERS)

    if r.status_code == 200:
         print(f"   ✅ Path '{path}' linked successfully.")
    else:
         print(f"   ❌ Failed to link path: {r.text}")


# Add Movies
add_library("Movies", "/movies", "movies")

# Add TV Shows
add_library("TV Shows", "/tv", "tvshows")

print("🔄 Triggering Scan...")
requests.post(f"{BASE_URL}/Library/Refresh", headers=HEADERS)
print("✅ Done.")
