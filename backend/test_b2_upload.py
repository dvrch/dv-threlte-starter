#!/usr/bin/env python3
"""
Test script to verify B2 upload functionality
"""

import os
import sys
import django
import requests
from pathlib import Path

# Setup Django
sys.path.append("/home/kd/Bureau/dv-threlte-starter")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


def test_b2_upload_endpoint():
    """Test the B2 upload endpoint with a small test file"""

    # Create a small test file
    test_file_path = "/tmp/test_upload.glb"
    with open(test_file_path, "wb") as f:
        f.write(b"fake glb content for testing")

    try:
        # Test the upload endpoint
        with open(test_file_path, "rb") as f:
            files = {"file": ("test.glb", f, "model/gltf-binary")}
            response = requests.post(
                "http://localhost:8000/api/storage/b2/upload/",
                files=files,
                data={"original_name": "test.glb"},
            )

        print(f"Upload response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Upload response: {response.json()}")
        else:
            print(f"Upload failed: {response.text}")

    except Exception as e:
        print(f"Error testing upload: {e}")
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def check_geometries():
    """Check current geometries and their B2 asset links"""
    from Base_threlte_dv.models import Geometry, B2Asset

    print("\n=== Current Geometries ===")
    geometries = Geometry.objects.all()
    for geom in geometries:
        print(f"Geometry: {geom.name} (type: {geom.type})")
        print(f"  - B2 Asset: {geom.b2_asset}")
        print(f"  - Cloudinary Asset: {geom.cloudinary_asset}")
        print(f"  - Current Asset URL: {geom.asset_url}")
        print(f"  - Asset Backend: {geom.asset_backend}")
        print()

    print("\n=== B2 Assets ===")
    b2_assets = B2Asset.objects.all()
    for asset in b2_assets:
        print(f"B2 Asset: {asset.original_name} -> {asset.url}")


if __name__ == "__main__":
    print("Testing B2 Upload Functionality")
    print("=" * 40)

    # Check current state
    check_geometries()

    # Test upload (only if Django server is running)
    # test_b2_upload_endpoint()

    print("\nTo test the upload endpoint:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Run: python test_b2_upload.py")
