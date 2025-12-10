#!/usr/bin/env python3
import os
import sys
import django
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "backend"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# Test Cloudinary configuration
print("=== Cloudinary Configuration Test ===")
print(f"CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
print(f"API_KEY: {os.environ.get('CLOUDINARY_API_KEY')}")
print(f"API_SECRET: {'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET'}")
print(f"USE_CLOUDINARY: {os.environ.get('USE_CLOUDINARY')}")

# Test Cloudinary connection
try:
    # Test with a simple text file
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("test file content")
        temp_path = f.name

    result = cloudinary.uploader.upload(
        temp_path,
        resource_type="raw",
        public_id="test-connection",
        folder="dv-threlte-test",
    )
    print(f"✅ Cloudinary upload successful: {result['url']}")

    # Clean up
    cloudinary.uploader.destroy("dv-threlte-test/test-connection", resource_type="raw")
    print("✅ Test file cleaned up")

except Exception as e:
    print(f"❌ Cloudinary upload failed: {e}")
    print(f"Error type: {type(e).__name__}")
