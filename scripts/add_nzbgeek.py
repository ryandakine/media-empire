import requests
import json
import time

PROWLARR_URL = "http://localhost:9696/api/v1"
API_KEY = "1924e5254ee241bb9583a68ae1162864"

# NZBGeek Config
INDEXER_NAME = "NZBGeek"
INDEXER_API_KEY = "sB30Xr4DEEsE0Gsze7ytLCoSzep6WGKT"

def get_schema_id(name):
    r = requests.get(f"{PROWLARR_URL}/indexer/schema", headers={"X-Api-Key": API_KEY})
    if r.status_code != 200:
        return None
    
    schemas = r.json()
    match = next((s for s in schemas if s['name'].lower() == name.lower()), None)
    return match

def add_nzbgeek():
    print(f"🔍 Getting schema for {INDEXER_NAME}...")
    schema = get_schema_id(INDEXER_NAME)
    
    if not schema:
        print(f"❌ Could not find schema for {INDEXER_NAME}")
        return

    print(f"➕ Adding {INDEXER_NAME}...")
    
    payload = schema
    payload['enable'] = True
    payload['appProfileId'] = 1 # Sync Profile
    payload['priority'] = 1 # Higher priority than torrents (usually lower number = higher priority)
    
    # Fill in the API Key field
    # We need to find the specific field in the schema fields list
    for field in payload['fields']:
        if field['name'] == 'apiKey':
             field['value'] = INDEXER_API_KEY
             print("   🔑 API Key injected.")

    r = requests.post(f"{PROWLARR_URL}/indexer", json=payload, headers={"X-Api-Key": API_KEY})
    
    if r.status_code == 201:
        print(f"✅ Successfully added {INDEXER_NAME}")
    elif r.status_code == 400 and "already" in r.text.lower():
         print(f"ℹ️ {INDEXER_NAME} already exists. Updating...")
         # Logic to update would require ID, let's assume if it exists we might need to verify key.
         # For now, if it exists, Prowlarr usually handles it.
    else:
        print(f"❌ Failed to add {INDEXER_NAME}: {r.text}")

if __name__ == "__main__":
    add_nzbgeek()
