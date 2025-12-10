#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from backend.Base_threlte_dv.models import Geometry, B2Asset


def link_geometries_to_b2():
    """Link geometries to their corresponding B2 assets"""

    # Mapping of geometry names to B2 asset file names
    geometry_to_b2 = {
        "bibi": "bibi.glb",
        "vague": "peagh-drap.glb",  # vague-9tykb was the old name
        "desk": "DRAP+Barrel Model1.glb",  # desk was the old name
        "icosahedron": None,  # No matching asset found
    }

    print("Linking geometries to B2 assets...")

    for geometry_name, b2_filename in geometry_to_b2.items():
        try:
            geometry = Geometry.objects.get(name=geometry_name)
            print(f"\nProcessing geometry: {geometry.name} (ID: {geometry.id})")

            if b2_filename:
                # Find the B2 asset
                try:
                    b2_asset = B2Asset.objects.get(file_name__endswith=b2_filename)
                    print(f"  Found B2 asset: {b2_asset.file_name} (ID: {b2_asset.id})")

                    # Link the geometry to the B2 asset
                    geometry.b2_asset = b2_asset
                    geometry.cloudinary_asset = None  # Remove Cloudinary link
                    geometry.save()

                    print(f"  ✓ Linked geometry to B2 asset")
                    print(f"  ✓ Asset URL: {geometry.asset_url}")

                except B2Asset.DoesNotExist:
                    print(f"  ✗ B2 asset not found for {b2_filename}")
            else:
                print(f"  ⚠ No B2 asset mapping for {geometry_name}")

        except Geometry.DoesNotExist:
            print(f"  ✗ Geometry not found: {geometry_name}")

    print("\nFinal geometry status:")
    for geo in Geometry.objects.all():
        asset_info = geo.get_asset_info()
        if asset_info:
            print(f"  {geo.name}: {asset_info['backend']} -> {asset_info['url']}")
        else:
            print(f"  {geo.name}: No asset linked")


if __name__ == "__main__":
    link_geometries_to_b2()
