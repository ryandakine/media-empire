import requests
import json

SAB_URL = "http://localhost:8085/sabnzbd/api"
API_KEY = "3ae9d87359b74130a1ba5e94e03a262c"

def check_sab_queue():
    print("Checking SABnzbd Queue...")
    params = {
        "mode": "queue",
        "output": "json",
        "apikey": API_KEY
    }
    try:
        r = requests.get(SAB_URL, params=params)
        data = r.json()
        queue = data.get('queue', {})
        print(f"Queue Status: {queue.get('status')}")
        print(f"Items: {queue.get('noofslots')}")
        
        for slot in queue.get('slots', []):
            print(f" - {slot['filename']} ({slot['percentage']}%) - {slot['status']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_sab_queue()
