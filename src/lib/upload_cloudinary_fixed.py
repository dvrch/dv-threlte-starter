#!/usr/bin/env python3
import os
import re
import cloudinary.uploader
from pathlib import Path

# Configuration
CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
API_KEY = os.getenv("CLOUDINARY_API_KEY")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Cloudinary folder as defined in cloudinaryAssets.ts
CLOUDINARY_TARGET_FOLDER = "dv-threlte/public"


def get_cleaned_path_for_cloudinary_public_id(path_relative_to_static: str) -> str:
    """
    Mimics the cleaning logic of getCloudinaryAssetUrl to determine the correct public_id.
    """
    # Remove common prefixes that should not be part of public_id
    cleaned_path = re.sub(
        r"^(public\/|assets\/|models\/)+", "", path_relative_to_static
    )
    # Remove leading/trailing slashes
    cleaned_path = cleaned_path.strip("/")
    return cleaned_path


def upload_file_to_cloudinary(file_path_relative_to_project_root):
    if not all([CLOUD_NAME, API_KEY, API_SECRET]):
        print("❌ Missing credentials")
        return

    cloudinary.config(
        cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET, secure=True
    )

    filepath = Path(file_path_relative_to_project_root)

    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        return

    # Get the path relative to 'static/'
    path_relative_to_static = str(filepath.relative_to("static"))

    # Determine the public_id using the same cleaning logic as the frontend
    public_id = get_cleaned_path_for_cloudinary_public_id(path_relative_to_static)

    # The Cloudinary folder should always be CLOUDINARY_TARGET_FOLDER
    folder = CLOUDINARY_TARGET_FOLDER

    print(
        f"⬆️  Uploading {filepath} to Cloudinary folder '{folder}' as public_id '{public_id}'..."
    )
    try:
        result = cloudinary.uploader.upload(
            str(filepath),
            public_id=public_id,
            resource_type="raw",  # Use 'raw' for GLB, 'image' for PNG/JPG
            folder=folder,
            overwrite=True,
            unique_filename=False,
            use_filename=True,  # This might be problematic if public_id is already set
        )
        print(f"✅ Success: {result['secure_url']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    files_to_upload = [
        "static/assets/garden.glb",
        "static/assets/ghost.glb",
        "static/public/mario.glb",
        "static/public/zaki.png",
        "static/public/cdn.glb",
        "static/public/cloth_sim.glb",
        "static/public/bibi.glb",
        "static/public/nissan.glb",
        "static/public/nissan2.glb",  # Added the missing file
        "static/public/bibi3.glb",
    ]

    for file_path in files_to_upload:
        upload_file_to_cloudinary(file_path)


if __name__ == "__main__":
    main()
