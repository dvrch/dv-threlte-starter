#!/usr/bin/env python3
"""
Script de test pour vérifier l'upload de fichiers vers Cloudinary
via l'API Django /api/geometries/
"""

import os
import requests
import json
from pathlib import Path

# Configuration
API_URL = "https://dv-threlte-starter-production.up.railway.app/api/geometries/"

# Créer un fichier GLB de test
test_file_path = "/tmp/test_upload.glb"
test_content = b"glTF mock content for testing upload"

with open(test_file_path, "wb") as f:
    f.write(test_content)

print(f"📁 Fichier de test créé : {test_file_path}")
print(f"📏 Taille : {len(test_content)} bytes")

# Préparer l'upload
with open(test_file_path, "rb") as f:
    files = {"model_file": ("test_upload.glb", f, "model/gltf-binary")}

    data = {
        "name": "test-cloudinary-upload",
        "type": "gltf_model",
        "model_type": "glb",
        "color": "#ff0000",
        "position": json.dumps({"x": 0, "y": 0, "z": 0}),
        "rotation": json.dumps({"x": 0, "y": 0, "z": 0}),
    }

    print("\n🚀 Envoi de la requête POST vers l'API Django...")
    print(f"🌐 URL : {API_URL}")

    try:
        response = requests.post(API_URL, files=files, data=data)

        print(f"\n📊 Statut de la réponse : {response.status_code}")
        print(f"📋 Headers : {dict(response.headers)}")

        if response.status_code == 201:
            result = response.json()
            print("\n✅ Succès ! Geometry créée :")
            print(json.dumps(result, indent=2))

            if result.get("asset"):
                print(f"\n🎯 Asset Cloudinary : {result['asset']}")
                print(f"🔗 URL du modèle : {result.get('model_url', 'N/A')}")
            else:
                print("\n⚠️  Attention : Aucun asset Cloudinary créé")

        else:
            print(f"\n❌ Erreur {response.status_code}")
            print(f"Réponse : {response.text}")

    except Exception as e:
        print(f"\n💥 Exception lors de l'upload : {e}")

# Nettoyer
os.remove(test_file_path)
print(f"\n🧹 Fichier de test supprimé : {test_file_path}")
