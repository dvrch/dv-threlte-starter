// src/routes/app/+page.server.js

import * as publicEnv from '$env/static/public';

export async function load({ fetch }) {
  const PUBLIC_STATIC_URL = publicEnv.PUBLIC_STATIC_URL || '';
  try {
    // L'URL de l'API est appelée côté serveur, il faut donc être explicite.
    const response = await fetch('http://127.0.0.1:8000/api/geometries/');

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // La pagination de DRF renvoie un objet avec `results`
    // On filtre pour ne garder que les géométries valides
    const validDynamicTypes = ['sphere', 'vague', 'tissus', 'desk', 'nissan', 'bibi', 'garden', 'nissangame', 'bibigame'];
    
    let geometries = (data.results || []).filter(geom => {
      if (geom.model_type === 'from_file') {
        // Si c'est un composant dynamique, son type doit être dans la liste blanche
        return geom.type && validDynamicTypes.includes(geom.type);
      }
      // Pour les autres types (gltf, primitives...), on les laisse passer
      return true;
    });

    // Ensure 'garden' type has a default model_url if it's missing
    geometries.forEach(geom => {
      if (geom.type === 'garden' && !geom.model_url) {
        geom.model_url = 'models/garden.glb';
      }
    });

    // Préfixer les model_url avec l'URL du Blob si elle est définie
    if (PUBLIC_STATIC_URL) {
      geometries = geometries.map(geom => {
        // Vérifie si model_url existe et n'est pas déjà une URL complète
        if (geom.model_url && !geom.model_url.startsWith('http')) {
          // Construit l'URL complète vers le Vercel Blob
          // geom.model_url est le chemin relatif du fichier, ex: 'models/my_model.glb'
          return { ...geom, model_url: `${PUBLIC_STATIC_URL}/${geom.model_url}` };
        }
        return geom;
      });
    }

    return {
      geometries,
    };

  } catch (error) {
    console.error("Could not fetch geometries:", error);
    return {
      geometries: [],
      error: "Impossible de charger les modèles 3D."
    };
  }
}
