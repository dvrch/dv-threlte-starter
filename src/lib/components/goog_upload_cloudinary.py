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
CLOUDINARY_TARGET_FOLDER = 'dv-threlte/public'

def get_cleaned_path_for_cloudinary_public_id(path_relative_to_static: str) -> str:
    """
    Mimics the cleaning logic of getCloudinaryAssetUrl to determine the correct public_id.
    """
    cleaned_path = path_relative_to_static
    cleaned_path = re.sub(r'^(public\/|assets\/|models\/)+', '', cleaned_path)
    return cleaned_path

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

    # Get the path relative to 'static/'
    path_relative_to_static = str(filepath.relative_to('static'))

    # Determine the public_id using the same cleaning logic as the frontend
    public_id_base = get_cleaned_path_for_cloudinary_public_id(path_relative_to_static)
    public_id = str(Path(public_id_base).with_suffix('')) # Remove extension for public_id

    # The Cloudinary folder should always be CLOUDINARY_TARGET_FOLDER
    folder = CLOUDINARY_TARGET_FOLDER
    
    print(f"⬆️  Uploading {filepath} to Cloudinary folder '{folder}' as public_id '{public_id}'...")
    try:
        result = cloudinary.uploader.upload(
            str(filepath),
            public_id=public_id,
            resource_type='raw', # Use 'raw' for GLB, 'image' for PNG/JPG
            folder=folder,
            overwrite=True,
            unique_filename=False,
            use_filename=True # This might be problematic if public_id is already set
        )
        print(f"✅ Success: {result['secure_url']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    files_to_upload = [
        'static/assets/garden.glb',
        'static/assets/ghost.glb',
        'static/public/mario.glb',
        'static/public/zaki.png',
        'static/public/cdn.glb',
        'static/public/cloth_sim.glb',
        'static/public/bibi.glb',
        'static/public/bibi2.glb',
        'static/public/bibi3.glb',
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