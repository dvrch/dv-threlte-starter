"""
Django signal pour synchroniser automatiquement les assets Cloudinary
après chaque upload via l'API d'upload.
"""

import os
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from requests.auth import HTTPBasicAuth
from django.db import transaction
from backend.Base_threlte_dv.models import CloudinaryAsset


@receiver(post_save, sender=CloudinaryAsset)
def sync_cloudinary_after_upload(sender, instance, created, **kwargs):
    """
    Déclenché quand un CloudinaryAsset est créé via l'API d'upload.
    Synchronise automatiquement tous les assets Cloudinary.
    """
    if created:
        print(f"🔄 Synchronisation automatique déclenchée par: {instance.public_id}")

        # Exécuter la synchronisation en arrière-plan
        try:
            sync_all_cloudinary_assets()
        except Exception as e:
            print(f"❌ Erreur synchronisation automatique: {str(e)}")


def sync_all_cloudinary_assets():
    """
    Synchronise tous les types d'assets Cloudinary avec la base de données
    """
    # Configuration Cloudinary
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        print("❌ Configuration Cloudinary manquante")
        return False

    # Récupérer tous les types d'assets
    resource_types = ["image", "video", "raw"]
    total_synced = 0

    with transaction.atomic():
        for resource_type in resource_types:
            api_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/resources/{resource_type}/upload"

            response = requests.get(
                api_url, auth=HTTPBasicAuth(api_key or "", api_secret or "")
            )
            if response.status_code != 200:
                print(
                    f"❌ Erreur API Cloudinary ({resource_type}): {response.status_code}"
                )
                continue

            data = response.json()
            synced_count = 0

            for asset in data.get("resources", []):
                # Nettoyer l'URL redondante
                clean_url = clean_cloudinary_url(asset.get("secure_url", ""))

                cloudinary_asset, created = CloudinaryAsset.objects.update_or_create(
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

                if created:
                    synced_count += 1
                    total_synced += 1
                    print(f"➕ Ajouté ({resource_type}): {asset['public_id']}")

            print(f"📊 {resource_type}: {synced_count} nouveaux assets")

    print(f"✅ Synchronisation automatique terminée: {total_synced} nouveaux assets")
    return True


def clean_cloudinary_url(url):
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
