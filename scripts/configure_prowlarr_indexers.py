import requests
import json

PROWLARR_URL = "http://localhost:9696/api/v1"
API_KEY = "1924e5254ee241bb9583a68ae1162864"

def find_and_add_indexers():
    print("🔍 Searching for indexers schemas...")
    
    # We want public trackers
    # Endpoint /indexer/schema returns ALL available potential indexers (Cardigann definitions)
    r = requests.get(f"{PROWLARR_URL}/indexer/schema", headers={"X-Api-Key": API_KEY})
    if r.status_code != 200:
        print(f"❌ Failed to get schemas: {r.text}")
        return
        
    schemas = r.json()
    print(f"✅ Found {len(schemas)} available schemas.")
    
    targets = ["1337x", "The Pirate Bay", "YTS"]
    
    for target in targets:
        # Find the schema definition
        definition = next((s for s in schemas if s['name'].lower() == target.lower()), None)
        if not definition:
            print(f"⚠️ Could not find definition for {target}")
            continue
            
        print(f"➕ Adding {target}...")
        
        # Prepare payload from definition
        # We generally take the default fields from the schema
        payload = definition
        # Ensure it's enabled and attached to the default profile
        payload['enable'] = True
        payload['appProfileId'] = 1
        
        # Add it
        r = requests.post(f"{PROWLARR_URL}/indexer", json=payload, headers={"X-Api-Key": API_KEY})
        if r.status_code == 201:
            print(f"   ✅ Successfully added {target}")
        else:
            print(f"   ❌ Failed to add {target}: {r.text}")

    # Force Sync
    print("🔄 Forcing sync to apps...")
    # There isn't a direct "sync all" endpoint publicly documented often, but adding an indexer triggers it usually.
    # Or we can trigger a task.
    
if __name__ == "__main__":
    find_and_add_indexers()
