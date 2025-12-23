import os
import cloudinary
import cloudinary.uploader
import re # Import regex module
from pathlib import Path

# Configuration
CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
API_KEY = os.getenv('CLOUDINARY_API_KEY')
API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

# Cloudinary folder as defined in cloudinaryAssets.ts
CLOUDINARY_TARGET_FOLDER = 'dv-threlte' # Main folder

def upload_file_to_cloudinary(file_path_relative_to_project_root):
    if not all([CLOUD_NAME, API_KEY, API_SECRET]):
        print("❌ Missing credentials")
        return

    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET,
        secure=True
    )
    
    filepath = Path(file_path_relative_to_project_root)
    
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        return

    # Determine public_id from path relative to 'static'
    relative_path = filepath.relative_to('static')
    public_id = str(relative_path.with_suffix('')).replace('\\', '/')
    
    # Determine resource_type based on file extension
    resource_type = 'raw'
    if filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        resource_type = 'image'
    
    print(f"⬆️  Uploading {filepath} to Cloudinary folder '{CLOUDINARY_TARGET_FOLDER}' as public_id '{public_id}'...")
    try:
        result = cloudinary.uploader.upload(
            str(filepath),
            public_id=public_id,
            resource_type=resource_type,
            folder=CLOUDINARY_TARGET_FOLDER,
            overwrite=True,
            unique_filename=False
        )
        print(f"✅ Success: {result['secure_url']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    files_to_upload = [
        'static/textures/energy-beam-opacity.png',
        'static/textures/bibi.png',
        'static/models/spaceship.glb',
        'static/models/nissan.glb',
        'static/models/bibi3.glb',
        '/static/public/nissan2.glb',
        'static/models/compos-hdr/hdrpersOutput.hdr'  # HDR environment for Premium effects
    ]
    
    for file_path in files_to_upload:
        upload_file_to_cloudinary(file_path)

if __name__ == '__main__':
    main()


# ---
# Le problème vient du fait que vous utilisez /bin/python (le Python du système) au lieu du Python de votre environnement virtuel (.venv), où la librairie 
# cloudinary
#  est installée. De plus, il faut charger les variables d'environnement (
# .env
# ) pour que l'authentification fonctionne.

# Voici la commande exacte à copier-coller pour que ça marche (elle charge les clés et utilise le bon Python) :

# bash
# export $(grep -v '^#' .env | xargs) && .venv/bin/python src/lib/components/goog_upload_cloudinary.py
# Explication rapide :
# export $(grep -v '^#' .env | xargs) : Lit votre fichier 
# .env
#  et charge les clés API (API_KEY, SECRET, etc.) en mémoire pour ce script.
# .venv/bin/python
#  : Force l'utilisation du Python de votre dossier .venv (celui qui a le module 
# cloudinary
# ).
# Le fichier 
# static/public/nissan.glb
#  que vous ciblez dans votre script existe bien, donc cela devrait fonctionner immédiatement ! 🚀
# ---
# relative_path = filepath.relative_to('static')
#    public_id = str(relative_path.with_suffix('')).replace('\\', '/')
