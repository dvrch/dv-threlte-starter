// src/routes/scene-3d/+page.server.js

export async function load({ fetch }) {
  try {
    // Remplacez l'URL par l'URL de votre API en production si nécessaire
    const response = await fetch('http://127.0.0.1:8000/api/geometries/');

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const geometries = await response.json();

    // La pagination de DRF renvoie un objet avec `results`
    return {
      geometries: geometries.results || [],
    };

  } catch (error) {
    console.error("Could not fetch geometries:", error);
    return {
      geometries: [],
      error: "Impossible de charger les modèles 3D."
    };
  }
}
