// src/lib/asset-helper.ts
import { dev } from '$app/environment';

// IMPORTANT : Vous devrez mettre l'URL de base de votre Vercel Blob ici.
// Idéalement, via une variable d'environnement avec le chemin public VITE_.
const BLOB_BASE_URL = import.meta.env.VITE_BLOB_BASE_URL || 'https://<remplacer-par-votre-url-vercel-blob>';

/**
 * Retourne l'URL d'un asset en fonction de l'environnement.
 * @param path Le chemin de l'asset comme s'il était à la racine du site (ex: '/images/logo.png')
 */
export function getAssetUrl(path: string): string {
  if (dev) {
    // --- En DÉVELOPPEMENT ---
    // On retourne simplement le chemin local. Le serveur de dev de Vite s'en occupe.
    return path;
  } else {
    // --- En PRODUCTION ---
    // On construit l'URL complète vers le Vercel Blob.
    if (path.startsWith('http://') || path.startsWith('https://')) {
      return path;
    }
    // On s'assure que le chemin commence bien par un slash.
    const cleanPath = path.startsWith('/') ? path : '/' + path;
    return `${BLOB_BASE_URL}${cleanPath}`;
  }
}
