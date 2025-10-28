#!/bin/bash

# Script pour lancer le backend Django et les deux frontends Svelte
# Il tue les processus existants sur les ports avant de les lancer.
# Optimisé pour l'émulateur de terminal 'konsole'.

# --- Configuration ---
PROJECT_ROOT="$(pwd)"
VENV_ACTIVATE="${PROJECT_ROOT}/backend/venv-backend/bin/activate"
FRONTEND1_DIR="${PROJECT_ROOT}/Base_threlte_dv"
FRONTEND2_DIR="${PROJECT_ROOT}/front-Film"

BACKEND_PORT=8000
FRONTEND1_PORT=5173
FRONTEND2_PORT=5174

# --- Logique ---

# Tuer les processus sur les ports
echo "Nettoyage des ports ${BACKEND_PORT}, ${FRONTEND1_PORT} et ${FRONTEND2_PORT}..."
fuser -k ${BACKEND_PORT}/tcp >/dev/null 2>&1
fuser -k ${FRONTEND1_PORT}/tcp >/dev/null 2>&1
fuser -k ${FRONTEND2_PORT}/tcp >/dev/null 2>&1
sleep 1 # Laisse un court instant pour que les ports se libèrent

# Lancer le Backend Django
echo "Lancement du backend Django..."
source "${VENV_ACTIVATE}" && \
python backend/films_backend/manage.py runserver ${BACKEND_PORT} &

# Lancer le Frontend 1 (Base_threlte_dv)
echo "Lancement du frontend 1 (Threlte)..."
cd "${FRONTEND1_DIR}" && \
pnpm run dev -- --port ${FRONTEND1_PORT} &

# Lancer le Frontend 2 (front-Film)
echo "Lancement du frontend 2 (Film)..."
cd "${FRONTEND2_DIR}" && \
pnpm run dev -- --port ${FRONTEND2_PORT} &

echo "Tous les services ont été lancés dans de nouveaux term:inaux 'konsole'."

