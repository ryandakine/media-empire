import requests
import json
import pprint

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
        print("✅ Authenticated")
        return True
    return False

def check_and_fix_library(name, expected_path):
    print(f"\n🔍 Checking Library: {name}")
    r = requests.get(f"{BASE_URL}/Library/VirtualFolders", headers=HEADERS)
    folders = r.json()
    
    target_folder = next((f for f in folders if f['Name'] == name), None)
    
    if not target_folder:
        print(f"   ⚠️ Library '{name}' NOT found. Creating...")
        # Create logic here if needed, but let's focus on path verification
        return

    print(f"   ✅ Library '{name}' found.")
    locations = target_folder.get('Locations', [])
    print(f"   📂 Current locations: {locations}")
    
    if expected_path in locations:
        print(f"   ✅ Path '{expected_path}' is ALREADY correctly linked.")
    else:
        print(f"   ⚠️ Path '{expected_path}' missing. Adding...")
        path_payload = {
            "Name": name,
            "Path": expected_path,
            "PathInfo": {"Path": expected_path}
        }
        r = requests.post(f"{BASE_URL}/Library/VirtualFolders/Paths", params={"RefreshLibrary": "true"}, json=path_payload, headers=HEADERS)
        if r.status_code == 204 or r.status_code == 200:
            print("   ✅ Path added successfully.")
        else:
            print(f"   ❌ Failed to add path: {r.status_code} {r.text}")

authenticate()
check_and_fix_library("Movies", "/movies")
check_and_fix_library("TV Shows", "/tv")
requests.post(f"{BASE_URL}/Library/Refresh", headers=HEADERS)
print("\n🔄 Scan triggered.")
