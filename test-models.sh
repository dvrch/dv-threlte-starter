#!/bin/bash

# Script pour tester les modèles 3D depuis l'API locale
echo "🔍 Test de l'API locale..."
API_URL="http://127.0.0.1:8001/api/geometries/"

# Récupérer les modèles avec model_url non null
echo "📦 Modèles disponibles avec model_url:"
curl -s "$API_URL" | jq '.[] | select(.model_url != null) | {id, name, model_url, has_glb: (.model_url | contains(".glb"))}'

echo ""
echo "🎯 Filtre des modèles 3D valides uniquement:"
curl -s "$API_URL" | jq '.[] | select(.model_url != null and (.model_url | test("\\.glb$|\\.gltf$")) | {id, name, model_url}'