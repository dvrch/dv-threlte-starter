#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append("/home/kd/Bureau/dv-threlte-starter/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Setup Django
django.setup()

from backend.Base_threlte_dv.models import B2Asset, Geometry


def find_unused_assets():
    """Find B2 assets that are not linked to any geometry"""
    print("Checking for unused B2 assets...")

    all_assets = B2Asset.objects.all()
    unused_assets = []

    for asset in all_assets:
        # Check if this asset is linked to any geometry
        linked_geometries = Geometry.objects.filter(b2_asset_id=asset.id)
        if not linked_geometries.exists():
            unused_assets.append(asset)

    print(f"\nFound {len(unused_assets)} unused B2 assets:")
    for asset in unused_assets:
        print(f"  {asset.file_name} (ID: {asset.id})")
        print(f"    URL: {asset.url}")

    return unused_assets


if __name__ == "__main__":
    find_unused_assets()
