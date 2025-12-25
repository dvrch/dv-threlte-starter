// src/routes/scene-3d/+page.server.js

import { env } from '$env/dynamic/public';

export async function load({ fetch }) {
  const PUBLIC_API_URL = env.PUBLIC_API_URL || '';

  if (!PUBLIC_API_URL) {
    console.warn('PUBLIC_API_URL not configured, returning empty geometries list in scene-3d');
    return {
      geometries: [],
      error: null
    };
  }

  try {
    const response = await fetch(`${PUBLIC_API_URL}/api/geometries/`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const geometries = await response.json();

    // La pagination de DRF renvoie un objet avec `results`
    return {
      geometries: geometries.results || [],
    };

  } catch (error) {
    console.error("Could not fetch geometries in scene-3d:", error);
    return {
      geometries: [],
      error: "Impossible de charger les modèles 3D."
    };
  }
}
