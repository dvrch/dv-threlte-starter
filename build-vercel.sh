#!/bin/bash
# Script de configuration pour Vercel

# Ce script est exécuté après chaque déploiement sur Vercel
# Il configure la base de données et collecte les fichiers statiques

set -e  # Sortir si une commande échoue

echo "🔧 Configuration du déploiement Vercel..."

# 1. Collecte des fichiers statiques
echo "📦 Collecte des fichiers statiques Django..."
cd backend
python manage.py collectstatic --noinput --clear

# 2. Migration de la base de données
echo "🗄️ Migration de la base de données..."
python manage.py migrate

# 3. Afficher les logs pour le débogage
echo "✅ Configuration Vercel terminée!"
