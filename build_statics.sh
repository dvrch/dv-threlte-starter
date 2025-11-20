#!/bin/bash
# Script pour collecter les statiques Django et les uploader sur Vercel Blob

# 1. Mettre en place l'environnement virtuel et installer les dépendances
echo "--- Mise en place de l'environnement Python ---"
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Collecter les fichiers statiques
echo "--- Lancement de collectstatic ---"
python manage.py collectstatic --noinput

# 3. Uploader sur Vercel Blob
# Le token est récupéré depuis les variables d'environnement de Vercel
echo "--- Upload des fichiers statiques sur Vercel Blob ---"
vercel blob upload staticfiles --token=$VERCEL_BLOB_READ_WRITE_TOKEN --yes

echo "--- Script statiques terminé ---"
