#!/bin/bash
# Script de configuration pour Vercel

# Ce script est exécuté après chaque déploiement sur Vercel
# Il configure la base de données et collecte les fichiers statiques

set -e  # Sortir si une commande échoue

echo "🔧 Configuration du déploiement Vercel..."

# Aller au répertoire du backend (fonctionne en local ET sur Vercel)
cd "$(dirname "$0")/backend"

# 1. Collecte des fichiers statiques
echo "📦 Collecte des fichiers statiques Django..."
python manage.py collectstatic --noinput --clear

# 2. Migration de la base de données
echo "🗄️ Migration de la base de données..."
python manage.py migrate

# 3. Créer le superuser s'il n'existe pas
echo "👤 Configuration du superuser..."
python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
import os

User = get_user_model()

ADMIN_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'kd')
ADMIN_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'dvrchipro@gmail.com')
ADMIN_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=ADMIN_USERNAME).exists():
    User.objects.create_superuser(ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
    print(f"✅ Superuser '{ADMIN_USERNAME}' créé!")
else:
    print(f"✅ Superuser '{ADMIN_USERNAME}' existe déjà")
PYEOF

echo "✅ Configuration Vercel terminée!"
