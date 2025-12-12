// src/lib/config.ts

// Récupère l'URL de base de l'API depuis les variables d'environnement de Vite.
// Le préfixe VITE_ est requis par Vite pour exposer les variables au code client.
const API_URL = import.meta.env.VITE_PUBLIC_API_URL;

// Vérification pour s'assurer que la variable est définie.
if (!API_URL) {
	console.error(
		'VITE_PUBLIC_API_URL is not defined. Please check your .env file or Vercel project settings.'
	);
}

// Centralisation de tous les endpoints de l'API.
export const ENDPOINTS = {
	GEOMETRIES: `${API_URL}/api/geometries/`,
	TYPES: `${API_URL}/api/types/`,
	TOGGLE_VISIBILITY: (id: number) => `${API_URL}/api/geometries/${id}/toggle-visibility/`
	// Ajoutez d'autres endpoints ici au besoin.
};

// Exportation de l'URL de base pour d'autres usages si nécessaire.
export { API_URL };
