// src/lib/asset-helper.ts
import { dev } from '$app/environment';

// IMPORTANT : Vous devrez mettre l'URL de base de votre Vercel Blob ici.
// Idéalement, via une variable d'environnement avec le chemin public VITE_.
const BLOB_BASE_URL = import.meta.env.VITE_BLOB_BASE_URL || import.meta.env.VITE_PUBLIC_STATIC_URL || 'https://w0cb58ft2bj7sg0v.public.blob.vercel-storage.com';

/**
 * Retourne l'URL d'un asset en fonction de l'environnement.
 * @param path Le chemin de l'asset comme s'il était à la racine du site (ex: '/images/logo.png')
 */

export function getAssetUrl(path: string): string {
  // 1. Si l'URL est déjà absolue (http/https), on la retourne telle quelle
  // C'est le cas pour les assets Vercel Blob
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }

  // 2. Si on est en développement local et qu'on a un path relatif
  if (dev) {
    // Si c'est un asset statique du dossier /static (commençant par /media),
    // Django le sert en dev. 
    // Vite proxy souvent /api mais pas forcément /media par défaut 
    // sauf si configuré dans vite.config.js.
    // Pour être sûr, on peut préfixer par l'URL de l'API Django si besoin,
    // MAIS standardement Vite le gère si c'est dans `public` ou via proxy.
    // ICI : on assume que 'path' est relatif à la racine du serveur web.
    return path;
  }

  // 3. En production (ou si on veut forcer le Blob même en dev via ENV)
  // On fallback sur le Blob si ce n'est pas une URL absolue
  if (!BLOB_BASE_URL || BLOB_BASE_URL.includes('<remplacer-par-votre-url-vercel-blob>')) {
    // Cas de secours si pas de config Blob
    return path;
  }

  const cleanPath = path.startsWith('/') ? path : '/' + path;
  return `${BLOB_BASE_URL}${cleanPath}`;
}
