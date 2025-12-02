#!/bin/bash
# Script de développement complet - Frontend + Backend

echo "🚀 Lancement du développement Threlte + Django"
echo "================================================"

# Créer deux processus
# 1. Django backend
# 2. SvelteKit frontend

# Vérifier si .env.local existe
if [ ! -f .env.local ]; then
    echo "⚠️ Création du fichier .env.local"
    cat > .env.local << 'EOF'
PUBLIC_API_URL="http://localhost:8000"
PUBLIC_STATIC_URL="https://w0cb58ft2bj7sg0v.public.blob.vercel-storage.com"
EOF
fi

# Lancer Django en arrière-plan
echo "📡 Démarrage du serveur Django (localhost:8000)..."
cd backend
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Lancer le frontend SvelteKit
cd ..
echo "🎨 Démarrage du serveur SvelteKit (localhost:5173)..."
npm run dev

# Nettoyer à la fermeture
trap "kill $DJANGO_PID" EXIT
