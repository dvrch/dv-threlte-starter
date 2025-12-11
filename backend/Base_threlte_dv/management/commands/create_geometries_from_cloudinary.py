from django.core.management.base import BaseCommand
from django.db import transaction
from backend.Base_threlte_dv.models import Geometry, CloudinaryAsset


class Command(BaseCommand):
    help = "Crée des geometries de test à partir des assets Cloudinary"

    def handle(self, *args, **options):
        self.stdout.write("🏗️  Création des geometries de test depuis Cloudinary...")

        created_count = 0

        with transaction.atomic():
            # Récupérer tous les assets 3D (GLB/GLTF)
            assets_3d = CloudinaryAsset.objects.filter(
                asset_type="raw", url__endswith=".glb"
            ) | CloudinaryAsset.objects.filter(asset_type="raw", url__endswith=".gltf")

            for asset in assets_3d:
                # Vérifier si une geometry existe déjà pour cet asset
                if Geometry.objects.filter(asset=asset).exists():
                    self.stdout.write(f"⏭️  {asset.public_id} déjà utilisé")
                    continue

                # Créer une nouvelle geometry
                geometry = Geometry.objects.create(
                    name=asset.file_name or asset.public_id.split("/")[-1],
                    asset=asset,
                    model_type="glb" if asset.url.endswith(".glb") else "gltf",
                    position={"x": 0.0, "y": 0.0, "z": 0.0},
                    rotation={"x": 0.0, "y": 0.0, "z": 0.0},
                    color="#000000",
                )

                created_count += 1
                self.stdout.write(f"✅ Créé: {geometry.name} → {asset.public_id}")

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Terminé: {created_count} nouvelles geometries créées"
            )
        )
