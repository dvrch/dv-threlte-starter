#!/bin/bash

# Test the Vercel deployment API endpoint
echo "Testing API on Vercel..."
curl -v https://dv-threlte-starter.vercel.app/api/geometries/

echo -e "\n\n===== Checking environment variables ====="
echo "DATABASE_URL is set: $([ ! -z "$DATABASE_URL" ] && echo 'YES' || echo 'NO')"
echo "BLOB_READ_WRITE_TOKEN is set: $([ ! -z "$BLOB_READ_WRITE_TOKEN" ] && echo 'YES' || echo 'NO')"
echo "SECRET_KEY is set: $([ ! -z "$SECRET_KEY" ] && echo 'YES' || echo 'NO')"

echo -e "\n===== Local test (for comparison) ====="
curl -v http://localhost:8000/api/geometries/
