import requests

BASE_URL = "http://localhost:8096"

def check_media():
    print("Checking Jellyfin Media...")
    # Auth
    auth_url = f"{BASE_URL}/Users/AuthenticateByName"
    headers = {
        "Content-Type": "application/json",
        "X-Emby-Authorization": 'MediaBrowser Client="TestScript", Device="Terminal", DeviceId="test1234", Version="1.0.0"'
    }
    r = requests.post(auth_url, json={"Username": "ryan", "Pw": "password123"}, headers=headers)
    
    if r.status_code == 200:
        token = r.json()['AccessToken']
        headers = {"X-Emby-Token": token}
        
        # Get Items
        r = requests.get(f"{BASE_URL}/Items", params={"Recursive": True, "IncludeItemTypes": "Movie,Series"}, headers=headers)
        items = r.json().get('Items', [])
        print(f"Found {len(items)} items in Jellyfin:")
        for i in items:
            print(f" - {i['Name']} ({i['Type']})")
            
    else:
        print("Auth failed.")

if __name__ == "__main__":
    check_media()
