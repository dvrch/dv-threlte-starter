#!/usr/bin/env python3
"""
Upload missing assets to B2
"""

import os
import requests
from pathlib import Path


def upload_to_b2(file_path: str, b2_name: str):
    """Upload file to B2 using direct API"""
    B2_BASE_URL = "https://f003.backblazeb2.com/file/43dvcapp/"

    try:
        with open(file_path, "rb") as f:
            # For now, just show what we would upload
            file_size = os.path.getsize(file_path)
            print(f"Would upload: {file_path} -> {b2_name} ({file_size} bytes)")
            print(f"B2 URL would be: {B2_BASE_URL}{b2_name}")
            return True
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False


def main():
    print("🔍 Checking for missing assets...")

    # Files mentioned in the database that need to be on B2
    missing_files = [
        # From database entries
        ("models/hhh_nxf9ww.glb", "hhb_nxf9ww.glb"),  # vague model
        ("models/bibigame.glb", "bibigame.glb"),  # bibigame model
        # Check if these exist locally
    ]

    print("\n📋 Files that should be uploaded to B2:")
    for local_path, b2_name in missing_files:
        full_path = f"/home/kd/Bureau/dv-threlte-starter/static/{local_path}"
        if os.path.exists(full_path):
            upload_to_b2(full_path, b2_name)
        else:
            print(f"❌ Local file not found: {full_path}")

    print("\n💡 To upload these files to B2:")
    print("1. Use the Railway B2 upload interface")
    print("2. Or run: b2 upload-file --bucket 43dvcapp <local-path> <b2-name>")


if __name__ == "__main__":
    main()
