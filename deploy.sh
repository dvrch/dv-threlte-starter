#!/bin/bash
# Script de déploiement Django sur Vercel

# 1. Installer les dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# 2. Créer les fichiers statiques
echo "🔨 Collecte des fichiers statiques..."
python backend/manage.py collectstatic --noinput

# 3. Migrer la base de données
echo "🗄️ Migration de la base de données..."
python backend/manage.py migrate

# 4. Créer un superuser (optionnel, pour admin)
# python backend/manage.py createsuperuser --noinput --username=admin --email=admin@example.com

echo "✅ Déploiement Django terminé!"
