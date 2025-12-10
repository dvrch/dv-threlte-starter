#!/usr/bin/env python3
"""
Test Backblaze B2 storage configuration
"""

import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


def test_b2_storage():
    print("=== Backblaze B2 Storage Test ===")

    # Check environment variables
    print(f"USE_B2_STORAGE: {os.environ.get('USE_B2_STORAGE')}")
    print(f"B2_BUCKET_NAME: {os.environ.get('B2_BUCKET_NAME')}")
    print(f"B2_ENDPOINT_URL: {os.environ.get('B2_ENDPOINT_URL')}")
    print(f"B2_KEY_ID: {'SET' if os.environ.get('B2_KEY_ID') else 'NOT SET'}")
    print(
        f"B2_APPLICATION_KEY: {'SET' if os.environ.get('B2_APPLICATION_KEY') else 'NOT SET'}"
    )

    # Check Django settings
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', None)}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', None)}")

    # Test storage backend
    try:
        from django.core.files.storage import default_storage

        # Test file creation
        test_content = b"Hello B2 Storage!"
        test_filename = "b2-test/test-file.txt"

        print(f"\nTesting file upload to {test_filename}...")

        # Save file
        from django.core.files.base import ContentFile

        saved_file = default_storage.save(test_filename, ContentFile(test_content))
        print(f"✅ File saved as: {saved_file}")

        # Get file URL
        file_url = default_storage.url(saved_file)
        print(f"✅ File URL: {file_url}")

        # Test file existence
        exists = default_storage.exists(saved_file)
        print(f"✅ File exists: {exists}")

        # Clean up
        default_storage.delete(saved_file)
        print("✅ Test file cleaned up")

        print("\n✅ B2 storage test successful!")
        return True

    except Exception as e:
        print(f"\n❌ B2 storage test failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False


if __name__ == "__main__":
    test_b2_storage()
