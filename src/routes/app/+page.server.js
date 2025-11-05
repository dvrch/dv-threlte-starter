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
    return {
      geometries: data.results || [],
    };

  } catch (error) {
    console.error("Could not fetch geometries:", error);
    return {
      geometries: [],
      error: "Impossible de charger les modèles 3D."
    };
  }
}
