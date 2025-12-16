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
        # Fallback to cloth_sim.glb if rffdfn version doesn't exist
        filepath = Path('static/public/cloth_sim.glb')
    
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        return

    # Force the public_id to match what the app expects: 'public/cloth_sim_rffdfn'
    # The app requests: https://res.cloudinary.com/.../upload/public/cloth_sim_rffdfn.glb
    # So we need folder='dv-threlte/public' (if that's the base) AND ID='cloth_sim_rffdfn'
    # OR if folder is just 'dv-threlte', we need ID='public/cloth_sim_rffdfn'.
    # Looking at the 404: /upload/public/cloth_sim_rffdfn.glb
    # It seems the folder structure in Cloudinary might be 'public' at the root or 'public' is part of the ID.
    # Let's assume standard Cloudinary 'folder' param usage. 
    # If I use folder='public', public_id='cloth_sim_rffdfn', URL is .../upload/v123/public/cloth_sim_rffdfn.glb
    
    public_id = 'cloth_sim_rffdfn'
    folder = 'public' 
    
    print(f"⬆️  Uploading {filepath} to folder '{folder}' as '{public_id}'...")
    try:
        result = cloudinary.uploader.upload(
            str(filepath),
            public_id=public_id,
            resource_type='raw',
            folder=folder,
            overwrite=True,
            unique_filename=False,
            use_filename=True 
        )
        print(f"✅ Success: {result['secure_url']}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    upload_target()


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