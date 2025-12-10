"""
Django signals pour synchroniser automatiquement les assets Cloudinary
"""

import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import requests
import json


@receiver(post_save, sender=None)
def cloudinary_asset_saved(sender, instance, created, **kwargs):
    """
    Déclenché quand un CloudinaryAsset est créé ou modifié
    """
    if sender.__name__ == "CloudinaryAsset" and created:
        print(f"✅ Nouvel asset Cloudinary ajouté: {instance.public_id}")


@receiver(post_delete, sender=None)
def cloudinary_asset_deleted(sender, instance, **kwargs):
    """
    Déclenché quand un CloudinaryAsset est supprimé
    """
    if sender.__name__ == "CloudinaryAsset":
        print(f"🗑️ Asset Cloudinary supprimé: {instance.public_id}")


def sync_cloudinary_assets():
    """
    Synchronise manuellement tous les assets Cloudinary avec la base de données
    """
    try:
        # Configuration Cloudinary
        cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
        api_key = os.environ.get("CLOUDINARY_API_KEY")
        api_secret = os.environ.get("CLOUDINARY_API_SECRET")

        if not all([cloud_name, api_key, api_secret]):
            print("❌ Configuration Cloudinary manquante")
            return False

        # Récupérer tous les assets depuis l'API Cloudinary
        api_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/resources/image/upload"

        # Utiliser basic auth correctement
        from requests.auth import HTTPBasicAuth

        response = requests.get(
            api_url, auth=HTTPBasicAuth(api_key or "", api_secret or "")
        )
        if response.status_code != 200:
            print(f"❌ Erreur API Cloudinary: {response.status_code}")
            return False

        data = response.json()
        synced_count = 0

        # Importer le modèle ici pour éviter les problèmes circulaires
        from .models import CloudinaryAsset

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
                print(f"➕ Ajouté: {asset['public_id']}")

        print(f"✅ Synchronisation terminée: {synced_count} nouveaux assets")
        return True

    except Exception as e:
        print(f"❌ Erreur synchronisation Cloudinary: {str(e)}")
        return False


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

    # Pattern à détecter et nettoyer
    redundant_prefix = "https:/res.cloudinary.com/drcok7moc"

    if redundant_prefix in url:
        # Extraire la partie après le préfixe redondant
        parts = url.split(redundant_prefix)
        if len(parts) > 1:
            return parts[1]  # Retourne "/models/hhh_dmydkc.glb"

    return url
