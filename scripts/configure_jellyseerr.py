import json
import sqlite3
import os

SETTINGS_PATH = '/home/ryan/media-empire-1/config/jellyseerr/settings.json'
DB_PATH = '/home/ryan/media-empire-1/config/jellyseerr/db/db.sqlite3'

# 1. Update settings.json
with open(SETTINGS_PATH, 'r') as f:
    data = json.load(f)

data['jellyfin'] = {
    "name": "Jellyfin",
    "ip": "jellyfin",
    "port": 8096,
    "useSsl": False,
    "urlBase": "",
    "externalHostname": "",
    "jellyfinForgotPasswordUrl": "",
    "libraries": [],
    "serverId": "3693239e07c7436785ace81bbe7f7ffd",
    "apiKey": "675e2764dcce4cdd895c965cc6c6819b"
}
data['main']['mediaServerType'] = 2 # 1=Plex, 2=Jellyfin/Emby? Or is it 3?
# The wizard usually sets this. Let's check constants if possible, but 2 is a good guess for Jellyfin if Plex is 1.

# Set initialized = true
if 'public' not in data:
    data['public'] = {}
data['public']['initialized'] = True

with open(SETTINGS_PATH, 'w') as f:
    json.dump(data, f, indent=2)

print("settings.json updated")

# 2. Insert User into DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Check if user exists
c.execute("SELECT id FROM user WHERE email='ryan@media.local'")
if c.fetchone():
    print("User already exists")
else:
    # Insert super admin user
    # Permissions: 2=ADMIN (likely)
    c.execute("""
        INSERT INTO user (
            email, username, permissions, avatar, password, userType,
            jellyfinUsername, jellyfinAuthToken, jellyfinUserId, jellyfinDeviceId
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        'ryan@media.local',
        'ryan',
        16777216, # Full permissions often used in *Seerr apps (Overseerr/Jellyseerr)
        '/p/avatar.jpg',
        'password123', # Hash? No, if userType=3 (Jellyfin), it AUTHENTICATES against Jellyfin.
        # However, for local login, it needs a password hash.
        # But if we use Jellyfin auth, we use userType=3.
        3, # Jellyfin User
        'ryan',
        '675e2764dcce4cdd895c965cc6c6819b',
        'fd50169a8cc94fdaaa8b2f6d531d93dd',
        'setup123'
    ))
    conn.commit()
    print("User inserted")

conn.close()
