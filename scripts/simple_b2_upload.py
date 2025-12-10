#!/usr/bin/env python3
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
APPLICATION_KEY_ID = os.getenv("B2_KEY_ID")
APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
BUCKET_NAME = "43dvcapp"


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
            content_type=get_content_type(local_path),
        )

        print(f"✅ Upload réussi: {local_path} -> {b2_path}")
        return file_info

    except Exception as e:
        print(f"❌ Erreur upload {local_path}: {e}")
        return None


def get_content_type(file_path):
    """Détermine le content type selon l'extension"""
    ext = file_path.lower().split(".")[-1]
    content_types = {
        "glb": "model/gltf-binary",
        "gltf": "model/gltf+json",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
        "obj": "model/obj",
        "fbx": "model/fbx",
    }
    return content_types.get(ext, "application/octet-stream")


def main():
    """Fonction principale"""
    if not APPLICATION_KEY_ID or not APPLICATION_KEY:
        print("❌ Variables d'environnement B2_KEY_ID et B2_APPLICATION_KEY requises")
        sys.exit(1)

    static_dir = Path("/home/kd/Bureau/dv-threlte-starter/static/public")

    if not static_dir.exists():
        print(f"❌ Dossier static non trouvé: {static_dir}")
        sys.exit(1)

    # Types de fichiers à uploader
    patterns = [
        "models/*.glb",
        "models/*.gltf",
        "models/*.obj",
        "models/*.fbx",
        "textures/*.png",
        "textures/*.jpg",
        "textures/*.jpeg",
        "textures/*.webp",
        "assets/**/*",
    ]

    uploaded_files = []
    failed_files = []

    for pattern in patterns:
        for file_path in static_dir.glob(pattern):
            if file_path.is_file():
                # Chemin relatif pour B2
                relative_path = file_path.relative_to(static_dir)
                b2_path = str(relative_path).replace("\\", "/")

                print(f"Upload de {file_path} vers {b2_path}")

                result = upload_file_to_b2(str(file_path), b2_path)
                if result:
                    uploaded_files.append(str(file_path))
                else:
                    failed_files.append(str(file_path))

    # Résumé
    print(f"\n📊 Résumé:")
    print(f"  ✅ Fichiers uploadés: {len(uploaded_files)}")
    print(f"  ❌ Échecs: {len(failed_files)}")

    if failed_files:
        print(f"\n❌ Fichiers en échec:")
        for f in failed_files:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
