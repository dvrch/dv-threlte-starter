"""
📤 Script d'upload vers Cloudinary
Upload fichiers 3D (.glb) et images depuis static/ vers Cloudinary.

Prérequis:
    pip install cloudinary

Usage:
    export CLOUDINARY_CLOUD_NAME=xxx
    export CLOUDINARY_API_KEY=xxx
    export CLOUDINARY_API_SECRET=xxx
    python scripts/upload-to-cloudinary.py
"""

import os
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Configuration
CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
API_KEY = os.getenv('CLOUDINARY_API_KEY')
API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

SOURCE_DIRS = [
    'static/models',
    'static/assets',
    'static/public',
    'static/fkisios',
    'static/textures',
]

def check_credentials():
    """Vérifie que les credentials Cloudinary sont configurés"""
    if not all([CLOUD_NAME, API_KEY, API_SECRET]):
        print("❌ Erreur: Credentials Cloudinary manquants\n")
        print("💡 1. Créer compte gratuit sur cloudinary.com")
        print("💡 2. Dashboard > Settings > Access Keys")
        print("💡 3. Copier Cloud Name, API Key, API Secret\n")
        print("💡 Définir les variables d'environnement:")
        print("   export CLOUDINARY_CLOUD_NAME='your-cloud-name'")
        print("   export CLOUDINARY_API_KEY='your-api-key'")
        print("   export CLOUDINARY_API_SECRET='your-api-secret'")
        return False
    return True

def upload_to_cloudinary():
    """Upload tous les fichiers vers Cloudinary"""
    print("🚀 Début de l'upload vers Cloudinary...\n")
    
    # Configuration Cloudinary
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET,
        secure=True
    )
    
    print(f"✅ Connecté à Cloudinary: {CLOUD_NAME}\n")
    
    uploaded = 0
    skipped = 0
    errors = 0
    total_files = 0
    
    # Compter fichiers
    for source_dir in SOURCE_DIRS:
        if Path(source_dir).exists():
            total_files += len(list(Path(source_dir).rglob('*.*')))
    
    print(f"📦 {total_files} fichiers trouvés\n")
    
    # Upload chaque dossier
    for source_dir in SOURCE_DIRS:
        source_path = Path(source_dir)
        
        if not source_path.exists():
            print(f"⚠️  Dossier ignoré: {source_dir} (inexistant)")
            continue
        
        print(f"\n📁 Traitement: {source_dir}/")
        
        # Parcourir tous les fichiers
        for filepath in source_path.rglob('*.*'):
            if filepath.is_file():
                # Chemin relatif pour Cloudinary
                relative_path = filepath.relative_to('static')
                public_id = str(relative_path.with_suffix('')).replace('\\', '/')
                
                try:
                    # Déterminer resource_type
                    resource_type = 'raw'  # Par défaut (GLB, etc.)
                    if filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                        resource_type = 'image'
                    elif filepath.suffix.lower() in ['.mp4', '.webm', '.mov']:
                        resource_type = 'video'
                    
                    # Upload
                    print(f"⬆️  [{uploaded + 1}/{total_files}] {relative_path}... ", end='', flush=True)
                    
                    result = cloudinary.uploader.upload(
                        str(filepath),
                        public_id=public_id,
                        resource_type=resource_type,
                        folder='dv-threlte',  # Dossier dans Cloudinary
                        overwrite=True,
                        unique_filename=False
                    )
                    
                    print(f"✅ {result['secure_url']}")
                    uploaded += 1
                    
                except cloudinary.exceptions.Error as e:
                    if 'already exists' in str(e).lower():
                        print(f"⏭️  Déjà uploadé")
                        skipped += 1
                    else:
                        print(f"❌ Erreur: {e}")
                        errors += 1
                except Exception as e:
                    print(f"❌ Erreur: {e}")
                    errors += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ Upload terminé !")
    print(f"   - Uploadés: {uploaded}/{total_files}")
    print(f"   - Déjà présents: {skipped}")
    print(f"   - Erreurs: {errors}")
    print(f"{'=' * 60}\n")
    
    # Afficher URL de base
    print(f"🌐 URL de base des fichiers:")
    print(f"   https://res.cloudinary.com/{CLOUD_NAME}/raw/upload/dv-threlte/")
    print(f"   https://res.cloudinary.com/{CLOUD_NAME}/image/upload/dv-threlte/")

if __name__ == '__main__':
    if check_credentials():
        upload_to_cloudinary()
