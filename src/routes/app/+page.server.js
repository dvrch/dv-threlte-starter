// src/routes/app/+page.server.js

import * as publicEnv from '$env/static/public';

export async function load({ fetch }) {
  const PUBLIC_STATIC_URL = publicEnv.PUBLIC_STATIC_URL || '';
  const PUBLIC_API_URL = publicEnv.PUBLIC_API_URL || '';

  console.log('DEBUG: PUBLIC_API_URL in +page.server.js:', PUBLIC_API_URL);

  try {
    // Si pas d'API_URL configurée, retourner un tableau vide au lieu de faire une requête
    // Cela évite les erreurs de connexion à localhost:8000 pendant le build
    if (!PUBLIC_API_URL) {
      console.warn('PUBLIC_API_URL not configured, returning empty geometries list');
      return {
        geometries: [],
        error: null
      };
    }
    
    const response = await fetch(`${PUBLIC_API_URL}/api/geometries/`);

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

    // Filter out geometries that are supposed to have a model_url but don't.
    geometries = geometries.filter(geom => {
      if (geom.model_type === 'gltf' || geom.model_type === 'from_file') {
        return !!geom.model_url;
      }
      return true;
    });



    return {
      geometries,
    };

  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error("Could not fetch geometries:", errorMessage);
    return {
      geometries: [],
      error: "Impossible de charger les modèles 3D."
    };
  }
}
