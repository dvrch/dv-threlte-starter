// src/routes/app/+page.server.js

export async function load({ fetch }) {
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
    
    const geometries = (data.results || []).filter(geom => {
      if (geom.model_type === 'from_file') {
        // Si c'est un composant dynamique, son type doit être dans la liste blanche
        return geom.type && validDynamicTypes.includes(geom.type);
      }
      // Pour les autres types (gltf, primitives...), on les laisse passer
      return true;
    });

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
