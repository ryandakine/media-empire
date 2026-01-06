import requests
import json

SAB_URL = "http://localhost:8085/sabnzbd/api"
API_KEY = "3ae9d87359b74130a1ba5e94e03a262c"

def add_server():
    print("🔌 Adding Eweka Server to SABnzbd...")
    
    # SABnzbd API 'add_server' or 'config' mode
    # Standard format: mode=config&name=server_name&keyword=server_param&value=...
    # But adding a new server is tricky via API in older versions.
    # We can try to set config directly.
    
    # Actually, let's verify if we can access the config first.
    # The safest way programmatically is to APPEND to sabnzbd.ini if API fails, 
    # but let's try API config mode.
    
    # Constructing arguments for a new server 'eweka'
    params = {
        "mode": "config",
        "name": "servers",
        "fenable": "1",
        "host": "news.eweka.nl",
        "port": "563",
        "username": "4111a95fbe673c9b",
        "password": "Peace2men",
        "ssl": "1",
        "connections": "30",
        "apikey": API_KEY
    }
    
    # SABnzbd API for adding servers usually involves passing a special string or multiple calls
    # Let's try the 'add_server' action if supported, or modify config sections.
    # The official way is typically formatting parameters like `servers.Start.host=...`
    
    # Let's try direct INI injection as backup if API requires complex payload.
    # But first, API check.
    
    try:
        # Check version/auth
        r = requests.get(SAB_URL, params={"mode": "version", "apikey": API_KEY})
        if r.status_code != 200 or "version" not in r.text:
            print("❌ API Auth failed or SABnzbd down.")
            return

        print("✅ SABnzbd Online. Injecting Config...")
        
        # We will append to sabnzbd.ini directly because it's guaranteed to work on restart
        # and avoids API documentation guessing for 'add_server' which varies by version.
        
        config_path = "/home/ryan/media-empire-1/config/sabnzbd/sabnzbd.ini"
        
        server_block = """
[[news.eweka.nl]]
name = Eweka
displayname = Eweka
host = news.eweka.nl
port = 563
timeout = 60
username = 4111a95fbe673c9b
password = Peace2men
encrypted = 1
connections = 30
ssl = 1
retention = 0
enable = 1
"""
        with open(config_path, "a") as f:
            f.write(server_block)
            
        print("✅ Configuration appended to sabnzbd.ini")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_server()
