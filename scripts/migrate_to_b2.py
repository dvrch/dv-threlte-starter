#!/usr/bin/env python3
"""
Script pour migrer les assets locaux/Cloudinary vers Backblaze B2
et mettre à jour les références dans les fichiers du projet
"""

import os
import sys
import django
import json
import re
import boto3
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration Django
sys.path.append("/home/kd/Bureau/dv-threlte-starter/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.conf import settings
from Base_threlte_dv.models import Geometry, B2Asset, CloudinaryAsset
from botocore.exceptions import NoCredentialsError, ClientError


class B2AssetMigrator:
    def __init__(self):
        self.b2_client = boto3.client(
            "s3",
            endpoint_url=getattr(settings, "AWS_S3_ENDPOINT_URL", None),
            aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
            aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            region_name=getattr(settings, "AWS_S3_REGION_NAME", None),
        )
        self.bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
        self.migrated_assets = []
        self.failed_uploads = []

    def upload_file_to_b2(
        self, file_path: str, b2_key: str, content_type: str = None
    ) -> Dict:
        """Upload un fichier vers B2"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

            # Déterminer le content type
            if not content_type:
                if file_path.endswith(".glb"):
                    content_type = "model/gltf-binary"
                elif file_path.endswith(".gltf"):
                    content_type = "model/gltf+json"
                elif file_path.endswith((".jpg", ".jpeg")):
                    content_type = "image/jpeg"
                elif file_path.endswith(".png"):
                    content_type = "image/png"
                elif file_path.endswith(".webp"):
                    content_type = "image/webp"
                else:
                    content_type = "application/octet-stream"

            # Upload vers B2
            with open(file_path, "rb") as file:
                self.b2_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    b2_key,
                    ExtraArgs={"ContentType": content_type, "ACL": "public-read"},
                )

            # Récupérer les informations du fichier uploadé
            response = self.b2_client.head_object(Bucket=self.bucket_name, Key=b2_key)

            # Construire l'URL publique
            base_url = (
                getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)
                or f"https://{getattr(settings, 'AWS_S3_ENDPOINT_URL', '').replace('https://', '')}"
            )

            if base_url.endswith("/"):
                base_url = base_url[:-1]

            public_url = f"{base_url}/{b2_key}"

            return {
                "success": True,
                "b2_file_id": response.get("ETag", "").strip('"'),
                "url": public_url,
                "file_size": response.get("ContentLength", 0),
                "checksum": response.get("ETag", "").strip('"'),
                "content_type": content_type,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def migrate_static_assets(self) -> None:
        """Migre tous les assets des dossiers static/"""
        static_root = Path("/home/kd/Bureau/dv-threlte-starter/static")

        # Types de fichiers à migrer
        asset_patterns = [
            "**/*.glb",
            "**/*.gltf",  # Modèles 3D
            "**/*.jpg",
            "**/*.jpeg",
            "**/*.png",
            "**/*.gif",
            "**/*.webp",  # Images
            "**/*.obj",
            "**/*.fbx",  # Autres formats 3D
        ]

        for pattern in asset_patterns:
            for file_path in static_root.glob(pattern):
                if file_path.is_file():
                    self.migrate_single_file(file_path)

    def migrate_single_file(self, file_path: Path) -> None:
        """Migre un fichier individuel vers B2"""
        relative_path = file_path.relative_to(
            Path("/home/kd/Bureau/dv-threlte-starter")
        )
        b2_key = str(relative_path)

        print(f"Migration de {file_path} -> {b2_key}")

        # Upload vers B2
        upload_result = self.upload_file_to_b2(str(file_path), b2_key)

        if upload_result["success"]:
            # Créer l'entrée B2Asset en base de données
            b2_asset = B2Asset.objects.create(
                b2_file_id=upload_result["b2_file_id"],
                file_name=b2_key,
                original_name=file_path.name,
                url=upload_result["url"],
                bucket_name=self.bucket_name,
                content_type=upload_result["content_type"],
                file_size=upload_result["file_size"],
                checksum=upload_result["checksum"],
                tags=["migrated", "static"],
                metadata={
                    "original_path": str(relative_path),
                    "migration_date": django.utils.timezone.now().isoformat(),
                },
            )

            self.migrated_assets.append(
                {
                    "file_path": str(file_path),
                    "b2_key": b2_key,
                    "b2_asset_id": b2_asset.id,
                    "url": upload_result["url"],
                }
            )

            print(f"✅ Upload réussi: {upload_result['url']}")

        else:
            self.failed_uploads.append(
                {"file_path": str(file_path), "error": upload_result["error"]}
            )
            print(f"❌ Erreur upload {file_path}: {upload_result['error']}")

    def migrate_cloudinary_assets(self) -> None:
        """Migre les assets Cloudinary existants vers B2"""
        cloudinary_assets = CloudinaryAsset.objects.all()

        for asset in cloudinary_assets:
            print(f"Migration de Cloudinary asset: {asset.public_id}")

            # Télécharger l'asset depuis Cloudinary
            try:
                import cloudinary
                import requests

                # Télécharger le fichier
                response = requests.get(asset.url, stream=True)
                if response.status_code == 200:
                    # Sauvegarder temporairement
                    temp_path = f"/tmp/{asset.file_name or asset.public_id}"
                    with open(temp_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Upload vers B2
                    b2_key = f"cloudinary/{asset.public_id}.{asset.format or 'bin'}"
                    upload_result = self.upload_file_to_b2(
                        temp_path, b2_key, asset.asset_type
                    )

                    if upload_result["success"]:
                        # Créer B2Asset
                        b2_asset = B2Asset.objects.create(
                            b2_file_id=upload_result["b2_file_id"],
                            file_name=b2_key,
                            original_name=asset.file_name,
                            url=upload_result["url"],
                            bucket_name=self.bucket_name,
                            content_type=asset.asset_type,
                            file_size=asset.file_size,
                            checksum=upload_result["checksum"],
                            tags=asset.tags + ["migrated", "from_cloudinary"],
                            metadata={
                                "cloudinary_public_id": asset.public_id,
                                "cloudinary_asset_id": asset.asset_id,
                                "migration_date": django.utils.timezone.now().isoformat(),
                            },
                        )

                        # Mettre à jour les géométries qui pointent vers cet asset
                        geometries = Geometry.objects.filter(cloudinary_asset=asset)
                        for geom in geometries:
                            geom.b2_asset = b2_asset
                            geom.save()

                        self.migrated_assets.append(
                            {
                                "cloudinary_public_id": asset.public_id,
                                "b2_key": b2_key,
                                "b2_asset_id": b2_asset.id,
                                "url": upload_result["url"],
                                "geometries_updated": geometries.count(),
                            }
                        )

                        print(
                            f"✅ Migration Cloudinary réussie: {upload_result['url']}"
                        )

                    # Nettoyer le fichier temporaire
                    os.remove(temp_path)

                else:
                    print(
                        f"❌ Erreur téléchargement Cloudinary: {response.status_code}"
                    )

            except Exception as e:
                print(f"❌ Erreur migration Cloudinary {asset.public_id}: {str(e)}")

    def update_code_references(self) -> None:
        """Met à jour les références dans le code source"""
        print("\n🔄 Mise à jour des références dans le code...")

        # Mapping des anciens chemins vers les nouvelles URLs B2
        path_mappings = {}
        for asset in self.migrated_assets:
            if "file_path" in asset:
                old_path = asset["file_path"].replace(
                    "/home/kd/Bureau/dv-threlte-starter/", ""
                )
                new_url = asset["url"]
                path_mappings[old_path] = new_url

        # Fichiers à mettre à jour
        files_to_update = [
            "/home/kd/Bureau/dv-threlte-starter/src/lib/components/models/ghost.svelte",
            "/home/kd/Bureau/dv-threlte-starter/src/lib/components/models/garden.svelte",
            "/home/kd/Bureau/dv-threlte-starter/src/lib/components/models/spaceship.svelte",
            "/home/kd/Bureau/dv-threlte-starter/src/routes/app/models/garden.svelte",
            "/home/kd/Bureau/dv-threlte-starter/src/routes/Spaceship/models/spaceship.svelte",
            "/home/kd/Bureau/dv-threlte-starter/src/routes/planet/Earth.svelte",
        ]

        for file_path in files_to_update:
            if os.path.exists(file_path):
                self.update_file_references(file_path, path_mappings)

    def update_file_references(
        self, file_path: str, path_mappings: Dict[str, str]
    ) -> None:
        """Met à jour les références dans un fichier spécifique"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Remplacer les références de modèles 3D
            for old_path, new_url in path_mappings.items():
                # Patterns pour useGltf
                patterns = [
                    f"useGltf('{old_path}')",
                    f'useGltf("{old_path}")',
                    f"useGltf('/{old_path}')",
                    f'useGltf("/{old_path}")',
                ]

                for pattern in patterns:
                    content = content.replace(pattern, f"useGltf('{new_url}')")

            # Si le contenu a changé, sauvegarder le fichier
            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Mis à jour: {file_path}")

        except Exception as e:
            print(f"❌ Erreur mise à jour {file_path}: {str(e)}")

    def generate_migration_report(self) -> None:
        """Génère un rapport de migration"""
        report = {
            "migration_date": django.utils.timezone.now().isoformat(),
            "summary": {
                "total_migrated": len(self.migrated_assets),
                "total_failed": len(self.failed_uploads),
                "bucket_name": self.bucket_name,
            },
            "migrated_assets": self.migrated_assets,
            "failed_uploads": self.failed_uploads,
        }

        # Sauvegarder le rapport
        report_path = "/home/kd/Bureau/dv-threlte-starter/b2_migration_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n📊 Rapport de migration sauvegardé: {report_path}")
        print(f"✅ {len(self.migrated_assets)} assets migrés avec succès")
        print(f"❌ {len(self.failed_uploads)} échecs de migration")


def main():
    """Fonction principale de migration"""
    print("🚀 Début de la migration vers Backblaze B2...")

    migrator = B2AssetMigrator()

    try:
        # 1. Migration des assets statiques
        print("\n📁 Migration des assets statiques...")
        migrator.migrate_static_assets()

        # 2. Migration des assets Cloudinary
        print("\n☁️ Migration des assets Cloudinary...")
        migrator.migrate_cloudinary_assets()

        # 3. Mise à jour des références dans le code
        print("\n🔄 Mise à jour des références dans le code...")
        migrator.update_code_references()

        # 4. Génération du rapport
        migrator.generate_migration_report()

        print("\n🎉 Migration terminée!")

    except Exception as e:
        print(f"\n💥 Erreur lors de la migration: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
