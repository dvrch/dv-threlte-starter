# backend/Base_threlte_dv/management/commands/link_geometries_to_assets.py

from django.core.management.base import BaseCommand
from backend.Base_threlte_dv.models import Geometry, CloudinaryAsset


class Command(BaseCommand):
    help = "Lie les géométries existantes aux assets Cloudinary correspondants"

    def handle(self, *args, **options):
        self.stdout.write("▶️  Liaison des géométries aux assets Cloudinary...")

        linked_count = 0
        not_found_count = 0

        for geometry in Geometry.objects.all():
            if geometry.asset:
                self.stdout.write(
                    f"  ✓ Geometry {geometry.id} ({geometry.name}) déjà liée"
                )
                continue

            # Chercher un asset Cloudinary par correspondance partielle
            # Les noms de géométrie sont souvent des IDs courts, essayer de trouver des assets correspondants
            asset_name = (
                geometry.name.lower().replace(" ", "").replace("(", "").replace(")", "")
            )

            # Chercher d'abord par correspondance exacte dans file_name
            asset = None
            assets = CloudinaryAsset.objects.filter(
                asset_type="raw", file_name__icontains=asset_name
            ).first()

            if assets:
                asset = assets
            else:
                # Chercher par correspondance dans public_id
                assets = CloudinaryAsset.objects.filter(
                    asset_type="raw", public_id__icontains=asset_name
                ).first()
                asset = assets

            # Si toujours rien, essayer avec "bibi" pour les tests
            if not asset and "bibi" in asset_name:
                asset = CloudinaryAsset.objects.filter(
                    asset_type="raw", public_id="dv-threlte/public/bibi.glb"
                ).first()

            if asset:
                geometry.asset = asset
                geometry.save(update_fields=["asset"])
                linked_count += 1
                self.stdout.write(
                    f"  ✅ Geometry {geometry.id} ({geometry.name}) → Asset {asset.public_id}"
                )
            else:
                not_found_count += 1
                self.stdout.write(
                    f"  ❌ Geometry {geometry.id} ({geometry.name}) - Aucun asset trouvé"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"🎉 Terminé : {linked_count} géométries liées, {not_found_count} non trouvées"
            )
        )
# tst