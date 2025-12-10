# Backblaze B2 Asset Management

This directory contains scripts and configuration for managing assets in Backblaze B2 storage.

## Setup

1. Install required dependencies:

```bash
pip install b2sdk
```

2. Configure environment variables:

```bash
export B2_APPLICATION_KEY_ID=your_app_key_id
export B2_APPLICATION_KEY=your_app_key
export B2_BUCKET_NAME=43dvcapp
```

## Scripts

### simple_b2_upload.py

Uploads files from `static/` directories to B2 bucket with proper prefixes:

- `static/models/` → `models/` prefix
- `static/textures/` → `textures/` prefix
- `static/assets/` → `assets/` prefix

### migrate_to_b2.py

Migrates existing Cloudinary assets to B2 storage and updates database references.

## Directory Structure

```
static/
├── models/     # 3D models (.glb, .gltf)
├── textures/   # Texture files (.png, .jpg, .webp)
└── assets/     # Other assets (sounds, videos)
```

## Usage

1. Place files in appropriate `static/` subdirectory
2. Run upload script:

```bash
python scripts/simple_b2_upload.py
```

3. Update `src/lib/config/b2-assets.ts` with new asset mappings
4. Create corresponding B2Asset database records
