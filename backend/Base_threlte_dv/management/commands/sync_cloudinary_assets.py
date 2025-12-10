from django.core.management.base import BaseCommand
from django.db import transaction
import os
import requests
from requests.auth import HTTPBasicAuth


class Command(BaseCommand):
    help = "Synchronise les assets Cloudinary avec la base de données"

    def handle(self, *args, **options):
        self.stdout.write("🔄 Début de la synchronisation Cloudinary...")

        try:
            # Configuration Cloudinary
            cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
            api_key = os.environ.get("CLOUDINARY_API_KEY")
            api_secret = os.environ.get("CLOUDINARY_API_SECRET")

            if not all([cloud_name, api_key, api_secret]):
                self.stdout.write(
                    self.style.ERROR("❌ Configuration Cloudinary manquante")
                )
                return

            # Récupérer tous les types d'assets depuis l'API Cloudinary
            resource_types = ["image", "video", "raw"]
            total_synced = 0

            # Importer le modèle pour éviter les problèmes circulaires
            from backend.Base_threlte_dv.models import CloudinaryAsset

            with transaction.atomic():
                for resource_type in resource_types:
                    api_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/resources/{resource_type}/upload"

                    response = requests.get(
                        api_url, auth=HTTPBasicAuth(api_key or "", api_secret or "")
                    )
                    if response.status_code != 200:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ Erreur API Cloudinary ({resource_type}): {response.status_code}"
                            )
                        )
                        continue

                    data = response.json()
                    synced_count = 0

                    for asset in data.get("resources", []):
                        # Nettoyer l'URL redondante
                        clean_url = self.clean_cloudinary_url(
                            asset.get("secure_url", "")
                        )

                        cloudinary_asset, created = (
                            CloudinaryAsset.objects.update_or_create(
                                public_id=asset["public_id"],
                                defaults={
                                    "asset_id": asset.get("asset_id", ""),
                                    "url": clean_url,
                                    "asset_type": asset.get("resource_type", "raw"),
                                    "file_name": asset.get("original_filename", ""),
                                    "format": asset.get("format", ""),
                                    "file_size": asset.get("bytes", 0),
                                },
                            )
                        )

                        if created:
                            synced_count += 1
                            total_synced += 1
                            self.stdout.write(
                                f"➕ Ajouté ({resource_type}): {asset['public_id']}"
                            )

                    self.stdout.write(
                        f"📊 {resource_type}: {synced_count} nouveaux assets"
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Synchronisation terminée: {total_synced} nouveaux assets au total"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erreur synchronisation Cloudinary: {str(e)}")
            )

    def clean_cloudinary_url(self, url):
        """
        Nettoie les URLs Cloudinary redondantes
        Transforme: https://res.cloudinary.com/drcok7moc/raw/upload/https:/res.cloudinary.com/drcok7moc/models/hhh_dmydkc.glb
        En:       /models/hhh_dmydkc.glb
        """
        if not url:
            return url

        # Pattern à détecter et nettoyer
        redundant_prefix = "https:/res.cloudinary.com/drcok7moc"

        if redundant_prefix in url:
            # Extraire la partie après le préfixe redondant
            parts = url.split(redundant_prefix)
            if len(parts) > 1:
                return parts[1]  # Retourne "/models/hhh_dmydkc.glb"

        return url
