#!/usr/bin/env python3
"""
Script simple pour uploader les assets vers Backblaze B2
"""

import os
import sys
from pathlib import Path


def create_upload_instructions():
    """Crée un fichier d'instructions pour l'upload B2"""

    instructions = """# Instructions d'upload vers Backblaze B2

## 1. Configuration B2
Assurez-vous d'avoir configuré vos clés B2 dans les variables d'environnement :
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY` 
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_ENDPOINT_URL` (https://s3.us-west-004.backblazeb2.com)
- `AWS_S3_CUSTOM_DOMAIN` (https://f001.backblazeb2.com/file/43dvcapp)

## 2. Upload des assets

### Méthode 1: Script Python (recommandé)
```bash
cd /home/kd/Bureau/dv-threlte-starter
python scripts/upload_to_b2.py
```

### Méthode 2: Interface Web Backblaze
1. Connectez-vous à votre compte Backblaze
2. Allez dans "B2 Cloud Storage"
3. Créez le bucket "43dvcapp" s'il n'existe pas
4. Uploadez les dossiers suivants :
   - `static/models/` → `models/`
   - `static/textures/` → `textures/`
   - `static/assets/` → `assets/`

## 3. Structure des fichiers sur B2

```
43dvcapp/
├── models/
│   ├── ghost.glb
│   ├── garden.glb
│   ├── spaceship.glb
│   ├── DcYcU.glb
│   ├── threlte.glb
│   ├── scene.gltf
│   ├── character.glb
│   ├── mob1.glb
│   ├── mob2.glb
│   ├── world.glb
│   ├── world0.glb
│   ├── world1.glb
│   ├── world2.glb
│   ├── mario.glb
│   ├── bibi.glb
│   ├── bibi3.glb
│   └── cloth_sim.glb
├── textures/
│   ├── star.png
│   ├── energy-beam-opacity.png
│   ├── sky.jpg
│   ├── mario.png
│   ├── bibi.png
│   └── diamond.jpg
└── assets/
    └── [autres assets...]
```

## 4. Vérification

Après l'upload, vérifiez que les URLs sont accessibles :
- https://f001.backblazeb2.com/file/43dvcapp/models/ghost.glb
- https://f001.backblazeb2.com/file/43dvcapp/textures/star.png

## 5. Mise à jour de la base de données

Une fois les assets uploadés, exécutez :
```bash
cd /home/kd/Bureau/dv-threlte-starter/backend
python manage.py shell
```

Puis dans le shell Django :
```python
from Base_threlte_dv.models import B2Asset
from django.utils import timezone

# Créer des entrées B2Asset pour les fichiers uploadés
assets_to_create = [
    {
        'b2_file_id': 'ghost_001',
        'file_name': 'models/ghost.glb',
        'original_name': 'ghost.glb',
        'url': 'https://f001.backblazeb2.com/file/43dvcapp/models/ghost.glb',
        'bucket_name': '43dvcapp',
        'content_type': 'model/gltf-binary',
        'tags': ['3d-model', 'character'],
    },
    # ... ajouter d'autres assets
]

for asset_data in assets_to_create:
    B2Asset.objects.create(**asset_data)

print("Assets B2 créés avec succès!")
```

## 6. Test final

Testez l'application pour vérifier que :
- Les modèles 3D se chargent correctement
- Les textures s'affichent
- Les URLs B2 sont utilisées
"""

    instructions_path = Path(
        "/home/kd/Bureau/dv-threlte-starter/B2_UPLOAD_INSTRUCTIONS.md"
    )

    try:
        with open(instructions_path, "w", encoding="utf-8") as f:
            f.write(instructions)
        print(f"✅ Instructions créées: {instructions_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur création instructions: {e}")
        return False


def create_simple_upload_script():
    """Crée un script d'upload simple utilisant b2sdk"""

    script_content = '''#!/usr/bin/env python3
"""
Script d'upload simple vers Backblaze B2
"""

import os
import sys
from pathlib import Path

try:
    from b2sdk.v1 import InMemoryAccountInfo, B2Api
    from b2sdk.v1.exception import MissingAccountData
except ImportError:
    print("❌ b2sdk non installé. Installez-le avec: pip install b2sdk")
    sys.exit(1)

# Configuration
APPLICATION_KEY_ID = os.getenv('B2_APPLICATION_KEY_ID')
APPLICATION_KEY = os.getenv('B2_APPLICATION_KEY')
BUCKET_NAME = '43dvcapp'

def upload_file_to_b2(local_path, b2_path):
    """Upload un fichier vers B2"""
    try:
        # Initialiser B2
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        
        # Autoriser
        b2_api.authorize_account("production", APPLICATION_KEY_ID, APPLICATION_KEY)
        
        # Obtenir le bucket
        bucket = b2_api.get_bucket_by_name(BUCKET_NAME)
        
        # Upload le fichier
        file_info = bucket.upload_local_file(
            local_file=local_path,
            file_name=b2_path,
            content_type=get_content_type(local_path)
        )
        
        print(f"✅ Upload réussi: {local_path} -> {b2_path}")
        return file_info
        
    except Exception as e:
        print(f"❌ Erreur upload {local_path}: {e}")
        return None

def get_content_type(file_path):
    """Détermine le content type selon l'extension"""
    ext = file_path.lower().split('.')[-1]
    content_types = {
        'glb': 'model/gltf-binary',
        'gltf': 'model/gltf+json',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'webp': 'image/webp',
        'obj': 'model/obj',
        'fbx': 'model/fbx',
    }
    return content_types.get(ext, 'application/octet-stream')

def main():
    """Fonction principale"""
    if not APPLICATION_KEY_ID or not APPLICATION_KEY:
        print("❌ Variables d'environnement B2_APPLICATION_KEY_ID et B2_APPLICATION_KEY requises")
        sys.exit(1)
    
    static_dir = Path('/home/kd/Bureau/dv-threlte-starter/static')
    
    if not static_dir.exists():
        print(f"❌ Dossier static non trouvé: {static_dir}")
        sys.exit(1)
    
    # Types de fichiers à uploader
    patterns = [
        'models/*.glb',
        'models/*.gltf', 
        'models/*.obj',
        'models/*.fbx',
        'textures/*.png',
        'textures/*.jpg',
        'textures/*.jpeg',
        'textures/*.webp',
        'assets/**/*'
    ]
    
    uploaded_files = []
    failed_files = []
    
    for pattern in patterns:
        for file_path in static_dir.glob(pattern):
            if file_path.is_file():
                # Chemin relatif pour B2
                relative_path = file_path.relative_to(static_dir)
                b2_path = str(relative_path).replace('\\\\', '/')
                
                print(f"Upload de {file_path} vers {b2_path}")
                
                result = upload_file_to_b2(str(file_path), b2_path)
                if result:
                    uploaded_files.append(str(file_path))
                else:
                    failed_files.append(str(file_path))
    
    # Résumé
    print(f"\\n📊 Résumé:")
    print(f"  ✅ Fichiers uploadés: {len(uploaded_files)}")
    print(f"  ❌ Échecs: {len(failed_files)}")
    
    if failed_files:
        print(f"\\n❌ Fichiers en échec:")
        for f in failed_files:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
'''

    script_path = Path("/home/kd/Bureau/dv-threlte-starter/scripts/simple_b2_upload.py")

    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)  # Rendre exécutable
        print(f"✅ Script d'upload créé: {script_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur création script: {e}")
        return False


def main():
    """Fonction principale"""
    print("📝 Création des fichiers d'aide pour l'upload B2...")

    # Créer les instructions
    create_upload_instructions()

    # Créer le script d'upload
    create_simple_upload_script()

    print(f"\n🎉 Fichiers créés!")
    print(f"\n📋 Prochaines étapes:")
    print(f"  1. Configurez vos clés B2 dans les variables d'environnement")
    print(f"  2. Exécutez le script d'upload: python scripts/simple_b2_upload.py")
    print(f"  3. Vérifiez que les URLs sont accessibles")
    print(f"  4. Mettez à jour la base de données avec les B2Asset")


if __name__ == "__main__":
    main()
