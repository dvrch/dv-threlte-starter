#!/bin/bash

# Script corrigé pour lancer le backend Django et le frontend Svelte.
# Tue les processus existants sur les ports avant de les lancer.

# --- Configuration ---
PROJECT_ROOT="$(pwd)"
VENV_ACTIVATE="${PROJECT_ROOT}/backend/venv/bin/activate"
BACKEND_DIR="${PROJECT_ROOT}/backend"

BACKEND_PORT=8000
FRONTEND_PORT=5173

# --- Logique ---

echo "Arrêt des anciens processus sur les ports ${BACKEND_PORT} et ${FRONTEND_PORT}..."
fuser -k ${BACKEND_PORT}/tcp >/dev/null 2>&1
fuser -k ${FRONTEND_PORT}/tcp >/dev/null 2>&1
sleep 1

# Lancer le Backend Django en arrière-plan
echo "Lancement du backend Django (http://localhost:${BACKEND_PORT})..."
(
  cd "${BACKEND_DIR}" && \
  source venv/bin/activate && \
  python manage.py runserver ${BACKEND_PORT}
) &

# Lancer le Frontend SvelteKit en arrière-plan
echo "Lancement du frontend SvelteKit (http://localhost:${FRONTEND_PORT})..."
(
  pnpm run dev -- --port ${FRONTEND_PORT}
) &

echo "Les services ont été lancés en arrière-plan."