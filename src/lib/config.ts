// src/lib/config.ts

// Récupère l'URL de base de l'API depuis les variables d'environnement de Vite.
// Le préfixe VITE_ est requis par Vite pour exposer les variables au code client.
const API_URL = import.meta.env.VITE_PUBLIC_API_URL || '';

if (!API_URL && typeof window !== 'undefined' && !window.location.hostname.includes('github.io')) {
	console.error(
		'VITE_PUBLIC_API_URL is not defined.'
	);
}

export const ENDPOINTS = {
	GEOMETRIES: API_URL ? `${API_URL}/api/geometries/` : '/api/geometries/',
	TYPES: API_URL ? `${API_URL}/api/types/` : '/api/types/',
	TOGGLE_VISIBILITY: (id: number) => API_URL ? `${API_URL}/api/geometries/${id}/toggle-visibility/` : `/api/geometries/${id}/toggle-visibility/`
};

// Exportation de l'URL de base pour d'autres usages si nécessaire.
export { API_URL };
