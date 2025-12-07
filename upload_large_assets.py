
import os
import requests
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env variables
load_dotenv(Path("backend") / ".env")

TOKEN = os.environ.get("BLOB_READ_WRITE_TOKEN")

if not TOKEN:
    print("❌ Error: BLOB_READ_WRITE_TOKEN not found in backend/.env")
    sys.exit(1)

FILES_TO_UPLOAD = [
    "static/public/cloth_sim.glb",
    "static/public/DRAP+Barrel Model1.glb", 
    "static/assets/Desk-bati.glb",
    "static/models/spaceship.glb",
    "static/models/nissan1.glb",
    "static/public/nissan2.glb",
    "static/models/nissan.glb",
    "static/assets/nissan.glb"
]

def upload_file(path_str):
    path = Path(path_str)
    if not path.exists():
        print(f"⚠️ File not found: {path} (Skipping)")
        return None

    filename = path.name
    # Decide folder based on extension or just put in 'static-assets'
    pathname = f"static-assets/{filename}"
    
    api_url = f"https://blob.vercel-storage.com/{pathname}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
    }

    print(f"📤 Uploading {filename} ({path.stat().st_size / (1024*1024):.2f} MB)...")
    
    try:
        with open(path, "rb") as f:
            response = requests.put(api_url, headers=headers, data=f)
            response.raise_for_status()
            blob_url = response.json().get("url")
            print(f"✅ Uploaded: {blob_url}")
            return (path_str, blob_url)
    except Exception as e:
        print(f"❌ Failed to upload {path}: {e}")
        return None

results = {}
for file_path in FILES_TO_UPLOAD:
    res = upload_file(file_path)
    if res:
        results[res[0]] = res[1]

print("\n--- SUMMARY OF UPLOADS ---")
for local_path, url in results.items():
    print(f"{local_path} => {url}")

print("\n--- JSON MAPPING ---")
import json
print(json.dumps(results, indent=2))
