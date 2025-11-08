#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# 0. Upload static assets to Vercel Blob
echo "---> Uploading static assets to Vercel Blob..."
bash scripts/upload_assets.sh

# 1. Build SvelteKit frontend
echo "---> Building SvelteKit frontend..."
pnpm run build

# 2. Install Python dependencies
echo "---> Installing Python dependencies..."
pip install -r requirements.txt

# 3. Run Django collectstatic
echo "---> Collecting Django static files..."
python3 backend/films_backend/manage.py collectstatic --noinput
