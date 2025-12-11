from django.core.management.base import BaseCommand
from django.db import transaction
from backend.Base_threlte_dv.models import CloudinaryAsset
import os


class Command(BaseCommand):
    help = "Reconstruit les URLs Cloudinary complètes à partir des public_id"

    def handle(self, *args, **options):
        self.stdout.write("🔧 Reconstruction des URLs Cloudinary complètes...")

        cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "drcok7moc")
        base_url = f"https://res.cloudinary.com/{cloud_name}/raw/upload"

        updated_count = 0

        with transaction.atomic():
            for asset in CloudinaryAsset.objects.all():
                # Reconstruire l'URL complète
                full_url = f"{base_url}/{asset.public_id}"

                if asset.url != full_url:
                    asset.url = full_url
                    asset.save(update_fields=["url"])
                    updated_count += 1
                    self.stdout.write(f"✅ {asset.public_id}: {full_url}")

        self.stdout.write(
            self.style.SUCCESS(f"✅ Terminé: {updated_count} URLs reconstruites")
        )
