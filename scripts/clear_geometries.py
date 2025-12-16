import os
import requests
import time

# URL from .env (hardcoded for safety as observed in .env viewing)
API_URL = "https://dv-threlte-starter-production.up.railway.app"
GEOMETRIES_ENDPOINT = f"{API_URL}/api/geometries/"

def clear_db():
    print(f"🔥 Clearing geometries from {GEOMETRIES_ENDPOINT}...")
    
    try:
        # 1. Fetch all geometries
        response = requests.get(GEOMETRIES_ENDPOINT, headers={'Accept': 'application/json'})
        if response.status_code != 200:
            print(f"❌ Failed to fetch: {response.status_code}")
            return

        geometries = response.json()
        
        # Handle pagination if necessary, though simpler is just to delete what we see
        results = geometries.get('results', geometries) if isinstance(geometries, dict) else geometries
        
        if not results:
            print("✨ Database is already empty.")
            return

        print(f"🗑️ Found {len(results)} geometries. Deleting...")

        count = 0
        for geo in results:
            geo_id = geo['id']
            # Delete request
            del_url = f"{GEOMETRIES_ENDPOINT}{geo_id}/"
            del_resp = requests.delete(del_url)
            
            if del_resp.status_code in [200, 204]:
                print(f"  ✅ Deleted {geo.get('name', 'Unknown')} ({geo_id})")
                count += 1
            else:
                print(f"  ❌ Failed to delete {geo_id}: {del_resp.status_code}")
        
        print(f"🎉 Done! Deleted {count} items.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clear_db()
