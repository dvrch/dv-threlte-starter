// src/lib/utils/assets.ts
import { base } from '$app/paths';

/**
 * Crée une URL absolue pour un asset local situé dans le dossier /static.
 * Gère correctement le `base` path de SvelteKit pour la production.
 * @param path - Le chemin de l'asset depuis la racine de /static (ex: 'models/mon_modele.glb')
 * @returns L'URL complète et correcte pour l'asset.
 */
export function getLocalAssetUrl(path: string): string {
	// S'assurer que le chemin n'a pas de slash au début, car `base` le gère.
	const cleanPath = path.startsWith('/') ? path.substring(1) : path;
	return `${base}/${cleanPath}`;
}
