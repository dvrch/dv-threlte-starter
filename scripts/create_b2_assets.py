#!/usr/bin/env python3
"""
Create B2Asset records for uploaded files
"""

import os
import sys
import uuid
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django

django.setup()

from backend.Base_threlte_dv.models import B2Asset


def create_b2_assets():
    """Create B2Asset records for all uploaded files"""

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
        if B2Asset.objects.filter(file_name=filename).exists():
            print(f"⏭️  Skipping {filename} (already exists)")
            skipped_count += 1
            continue

        # Create B2Asset record
        try:
            asset = B2Asset.objects.create(
                b2_file_id=str(uuid.uuid4()),
                file_name=filename,
                original_name=filename,
                url=b2_url,
                bucket_name="43dvcapp",
                content_type=asset_type,
                file_size=0,  # We don't have the file size readily available
            )
            print(f"✅ Created B2Asset for {filename}")
            created_count += 1
        except Exception as e:
            print(f"❌ Failed to create B2Asset for {filename}: {e}")

    print(f"\n📊 Summary:")
    print(f"✅ Created: {created_count}")
    print(f"⏭️  Skipped: {skipped_count}")
    print(f"📋 Total B2Assets: {B2Asset.objects.count()}")


if __name__ == "__main__":
    create_b2_assets()
