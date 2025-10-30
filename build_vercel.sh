#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Install Python dependencies
echo "---> Installing Python dependencies..."
pip install -r requirements.txt

# 2. Run Django collectstatic
echo "---> Collecting Django static files..."
python3 backend/films_backend/manage.py collectstatic --noinput

# 3. Build SvelteKit frontend
echo "---> Building SvelteKit frontend..."
pnpm run build
