#!/usr/bin/env python3
"""
Quick B2 upload script for all assets
"""

import os
from pathlib import Path
from b2sdk.v1 import InMemoryAccountInfo, B2Api

# Configuration
APPLICATION_KEY_ID = os.getenv("B2_KEY_ID")
APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
BUCKET_NAME = "43dvcapp"


def upload_assets():
    """Upload all assets to B2"""
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", APPLICATION_KEY_ID, APPLICATION_KEY)
    bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

    static_public = Path("static/public")
    uploaded = []
    failed = []

    # Upload all files
    for file_path in static_public.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [
            ".glb",
            ".gltf",
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        ]:
            relative_path = file_path.relative_to(static_public)
            b2_path = str(relative_path).replace("\\", "/")

            try:
                file_info = bucket.upload_local_file(str(file_path), b2_path)
                uploaded.append(str(file_path))
                print(f"✅ {b2_path}")
            except Exception as e:
                failed.append(f"{file_path}: {e}")
                print(f"❌ {b2_path}: {e}")

    print(f"\n📊 Upload Summary:")
    print(f"✅ Uploaded: {len(uploaded)}")
    print(f"❌ Failed: {len(failed)}")

    if failed:
        print("\nFailed files:")
        for f in failed:
            print(f"  - {f}")


if __name__ == "__main__":
    upload_assets()
