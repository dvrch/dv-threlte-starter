#!/usr/bin/env python3
"""
Upload HDR file to Cloudinary
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

import cloudinary
import cloudinary.uploader

# Upload HDR
hdr_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'models', 'compos-hdr', 'hdrpersOutput.hdr')

print(f"📤 Uploading {hdr_path} to Cloudinary...")

result = cloudinary.uploader.upload(
    hdr_path,
    folder="dv-threlte-starter",
    resource_type="raw",
    public_id="hdrpersOutput",
    overwrite=True
)

print(f"✅ HDR uploaded successfully!")
print(f"🔗 URL: {result['secure_url']}")
print(f"📦 Public ID: {result['public_id']}")
