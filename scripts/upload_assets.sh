#!/bin/bash
# scripts/upload_assets.sh

# Quitte le script si une commande échoue
set -e

echo "--- Début du téléversement des assets statiques vers Vercel Blob ---"

# Vérifier si le token est défini
if [ -z "$BLOB_READ_WRITE_TOKEN" ]; then
  echo "Erreur : La variable d'environnement BLOB_READ_WRITE_TOKEN n'est pas définie."
  echo "Veuillez l'ajouter dans les paramètres de votre projet Vercel."
  exit 1
fi

echo "Installation de la CLI Vercel..."
npm install -g vercel

ASSET_DIR="static"

# Vérifie si le dossier existe
if [ ! -d "$ASSET_DIR" ]; then
  echo "Dossier des assets '$ASSET_DIR' non trouvé. Le téléversement est annulé."
  exit 0
fi

# Navigue dans le dossier pour obtenir les chemins relatifs
cd "$ASSET_DIR"

# Trouve tous les fichiers et les téléverse un par un
# Le `pathname` dans le Blob store sera relatif au dossier ASSET_DIR
# ex: 'models/scene.gltf' sera téléversé avec le même chemin.
find . -type f | while read -r file; do
  # Retire le './' du début pour un chemin plus propre
  pathname="${file#./}"

  # Ignore les fichiers système comme .DS_Store
  if [[ "$pathname" == ".DS_Store" ]]; then
    continue
  fi

  echo "Téléversement de '$pathname'..."
  # Utilise le token BLOB_READ_WRITE_TOKEN que Vercel fournit durant le build
  # Le pathname dans le store est explicitement défini pour garantir la structure
  vercel blob put "$pathname" --pathname "$pathname" --token "$BLOB_READ_WRITE_TOKEN" --force
done
echo "--- Téléversement des assets terminé ---"

# Retourne au dossier précédent
cd - > /dev/null
