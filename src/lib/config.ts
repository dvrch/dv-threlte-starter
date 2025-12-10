// src/lib/config.ts

import { getB2AssetUrl, hasB2Asset } from './config/b2-assets';

// Récupère l'URL de base de l'API depuis les variables d'environnement de Vite.
// Le préfixe VITE_ est requis par Vite pour exposer les variables au code client.
const API_URL = import.meta.env.VITE_PUBLIC_API_URL;

// Vérification pour s'assurer que la variable est définie.
if (!API_URL) {
	console.error(
		'VITE_PUBLIC_API_URL is not defined. Please check your .env file or Vercel project settings.'
	);
}

// Configuration du stockage d'assets
const ASSET_STORAGE = import.meta.env.VITE_ASSET_STORAGE || 'b2'; // 'b2', 'local', 'cloudinary'

// Centralisation de tous les endpoints de l'API.
export const ENDPOINTS = {
	GEOMETRIES: `${API_URL}/api/geometries/`,
	TYPES: `${API_URL}/api/types/`,
	STORAGE_B2: `${API_URL}/api/storage/b2/`, // Proxy B2 endpoint
	B2_ASSETS: `${API_URL}/api/b2-assets/`,
	UPLOAD_B2: `${API_URL}/api/storage/b2/upload/` // B2 upload endpoint
	// Ajoutez d'autres endpoints ici au besoin.
};

// Système de gestion d'assets unifié
export class AssetManager {
	static getAssetUrl(assetPath: string): string {
		// Remove leading slash if present
		const cleanPath = assetPath.startsWith('/') ? assetPath.slice(1) : assetPath;

		switch (ASSET_STORAGE) {
			case 'b2':
				// Try B2 first, fallback to proxy
				if (hasB2Asset(cleanPath)) {
					return getB2AssetUrl(cleanPath);
				}
				return `${ENDPOINTS.STORAGE_B2}${cleanPath}`;

			case 'cloudinary':
				// Cloudinary URLs would go here
				return `https://res.cloudinary.com/your-cloud/raw/upload/${cleanPath}`;

			case 'local':
			default:
				// Local/static assets
				return `/${assetPath}`;
		}
	}

	static getStorageType(): string {
		return ASSET_STORAGE;
	}
}

// Exportation de l'URL de base pour d'autres usages si nécessaire.
export { API_URL };
