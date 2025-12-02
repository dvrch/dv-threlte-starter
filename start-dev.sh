#!/bin/bash
# 🚀 Script de démarrage complet du projet local
# Lance Django backend + SvelteKit frontend dans des processus séparés

set -e  # Sortir si une commande échoue

echo "🚀 Démarrage de Threlte 3D + Django + SvelteKit"
echo "==============================================="

# Déterminer le chemin Python
PYTHON="/home/kd/Bureau/dv-threlte-starter/.venv/bin/python"
PROJECT_DIR="/home/kd/Bureau/dv-threlte-starter"

# Créer .env.local s'il n'existe pas
if [ ! -f "$PROJECT_DIR/.env.local" ]; then
    echo "✅ Création de .env.local..."
    cat > "$PROJECT_DIR/.env.local" << 'EOF'
PUBLIC_API_URL="http://localhost:8000"
PUBLIC_STATIC_URL="https://w0cb58ft2bj7sg0v.public.blob.vercel-storage.com"
EOF
fi

# Fonction pour afficher les instructions
show_urls() {
    echo ""
    echo "✅ Services démarrés avec succès!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Frontend SvelteKit:"
    echo "   http://localhost:5173"
    echo "   ➜ Aller à http://localhost:5173/app pour voir la scène 3D"
    echo ""
    echo "📡 Backend Django:"
    echo "   http://localhost:8000"
    echo "   ➜ API: http://localhost:8000/api/geometries/"
    echo "   ➜ Admin: http://localhost:8000/admin/"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Trap pour nettoyer les processus à la fermeture
cleanup() {
    echo ""
    echo "🛑 Arrêt des services..."
    if [ ! -z "$DJANGO_PID" ]; then
        kill $DJANGO_PID 2>/dev/null || true
    fi
    if [ ! -z "$VITE_PID" ]; then
        kill $VITE_PID 2>/dev/null || true
    fi
    echo "✅ Services arrêtés"
    exit 0
}

trap cleanup INT TERM

# Lancer Django en arrière-plan
echo "📡 Démarrage du serveur Django..."
cd "$PROJECT_DIR/backend"
$PYTHON manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &
DJANGO_PID=$!

# Attendre que Django démarre
sleep 2

# Vérifier que Django a démarré
if ! ps -p $DJANGO_PID > /dev/null; then
    echo "❌ Erreur: Django n'a pas pu démarrer"
    cat /tmp/django.log
    exit 1
fi

# Lancer le frontend SvelteKit
echo "🎨 Démarrage du serveur SvelteKit..."
cd "$PROJECT_DIR"
npm run dev > /tmp/vite.log 2>&1 &
VITE_PID=$!

# Attendre que Vite démarre
sleep 3

# Vérifier que Vite a démarré
if ! ps -p $VITE_PID > /dev/null; then
    echo "❌ Erreur: SvelteKit n'a pas pu démarrer"
    cat /tmp/vite.log
    kill $DJANGO_PID
    exit 1
fi

# Afficher les URLs
show_urls

# Afficher les logs en temps réel
tail -f /tmp/django.log /tmp/vite.log 2>/dev/null || wait
