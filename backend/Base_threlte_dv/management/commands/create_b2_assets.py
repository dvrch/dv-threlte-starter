from django.core.management.base import BaseCommand
from Base_threlte_dv.models import B2Asset


class Command(BaseCommand):
    help = "Create B2Asset records for uploaded files"

    def handle(self, *args, **options):
        # B2 base URL
        b2_base_url = "https://s3.us-west-003.backblazeb2.com/43dvcapp"

        # List of uploaded files
        uploaded_files = [
            "bibi.png",
            "nissan2.glb",
            "Barrel Model1.glb",
            "hero-bg.webp",
            "Tout.jpg",
            "tete2porc.png",
            "Barrel Model+.glb",
            "cloth_sim.glb",
            "bibi3.glb",
            "mario.png",
            "hero-bg.jpg",
            "bibi.glb",
            "zaki.png",
            "cdn.glb",
            "bibi2.glb",
            "DRAP+Barrel Model1.glb",
            "diamond.jpg",
            "mario.glb",
            "diamond.webp",
            "peagh-drap.glb",
        ]

        created_count = 0
        skipped_count = 0

        for filename in uploaded_files:
            # Determine file type
            ext = filename.lower().split(".")[-1]
            if ext in ["glb", "gltf"]:
                asset_type = "model"
            elif ext in ["png", "jpg", "jpeg", "webp"]:
                asset_type = "texture"
            else:
                asset_type = "other"

            # Create B2 URL
            b2_url = f"{b2_base_url}/{filename}"

            # Check if asset already exists
            if B2Asset.objects.filter(filename=filename).exists():
                self.stdout.write(f"⏭️  Skipping {filename} (already exists)")
                skipped_count += 1
                continue

            # Create B2Asset record
            try:
                asset = B2Asset.objects.create(
                    filename=filename,
                    b2_url=b2_url,
                    asset_type=asset_type,
                    file_size=0,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created B2Asset for {filename}")
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to create B2Asset for {filename}: {e}")
                )

        self.stdout.write("\n📊 Summary:")
        self.stdout.write(self.style.SUCCESS(f"✅ Created: {created_count}"))
        self.stdout.write(f"⏭️  Skipped: {skipped_count}")
        self.stdout.write(f"📋 Total B2Assets: {B2Asset.objects.count()}")
