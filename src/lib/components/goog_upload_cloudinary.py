import os
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Configuration
CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
API_KEY = os.getenv('CLOUDINARY_API_KEY')
API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

def upload_target():
    if not all([CLOUD_NAME, API_KEY, API_SECRET]):
        print("❌ Missing credentials")
        return

    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET,
        secure=True
    )
    
    filepath = Path('static/public/cloth_sim_rffdfn.glb')
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        return

    relative_path = filepath.relative_to('static')
    public_id = str(relative_path.with_suffix('')).replace('\\', '/')
    
    print(f"⬆️  Uploading {filepath} as {public_id}...")
    try:
        result = cloudinary.uploader.upload(
            str(filepath),
            public_id=public_id,
            resource_type='raw',
            folder='dv-threlte',
            overwrite=True,
            unique_filename=False
        )
        print(f"✅ Success: {result['secure_url']}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    upload_target()
