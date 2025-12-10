# Instructions d'upload vers Backblaze B2

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
