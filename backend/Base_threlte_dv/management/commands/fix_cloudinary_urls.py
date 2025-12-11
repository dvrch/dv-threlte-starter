from django.core.management.base import BaseCommand
from django.db import transaction
from backend.Base_threlte_dv.models import Geometry, CloudinaryAsset


class Command(BaseCommand):
    help = (
        "Met à jour les URLs des assets Cloudinary pour corriger les chemins redondants"
    )

    def handle(self, *args, **options):
        self.stdout.write("🔧 Correction des URLs Cloudinary...")

        updated_count = 0

        with transaction.atomic():
            for asset in CloudinaryAsset.objects.all():
                original_url = asset.url
                clean_url = self.clean_cloudinary_url(original_url)

                if original_url != clean_url:
                    asset.url = clean_url
                    asset.save(update_fields=["url"])
                    updated_count += 1
                    self.stdout.write(
                        f"✅ {asset.public_id}: {original_url} → {clean_url}"
                    )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Terminé: {updated_count} URLs corrigées")
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
