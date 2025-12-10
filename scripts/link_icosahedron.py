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


def link_icosahedron():
    """Link the icosahedron geometry to an unused B2 asset"""
    print("Linking icosahedron geometry...")

    try:
        # Find the icosahedron geometry
        icosahedron = Geometry.objects.get(name="icosahedron")
        print(f"Found icosahedron geometry: ID {icosahedron.id}")

        # Find an unused GLB asset (mario.glb seems appropriate)
        mario_asset = B2Asset.objects.get(file_name="mario.glb")
        print(f"Found mario.glb asset: ID {mario_asset.id}")

        # Link them
        icosahedron.b2_asset_id = mario_asset.id
        icosahedron.b2_url = mario_asset.url
        icosahedron.save()

        print(f"✓ Successfully linked icosahedron to mario.glb")
        print(f"  Geometry ID: {icosahedron.id}")
        print(f"  Asset ID: {mario_asset.id}")
        print(f"  URL: {mario_asset.url}")

        return True

    except Geometry.DoesNotExist:
        print("❌ icosahedron geometry not found")
        return False
    except B2Asset.DoesNotExist:
        print("❌ mario.glb asset not found")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    success = link_icosahedron()
    if success:
        print("\n✅ Icosahedron linking completed successfully!")
    else:
        print("\n❌ Failed to link icosahedron")
