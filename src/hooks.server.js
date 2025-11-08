import { dev } from '$app/environment';

// URL de base de votre Vercel Blob Storage
const BLOB_BASE_URL = 'https://w0cb58ft2bj7sg0v.public.blob.vercel-storage.com';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
  const { pathname } = event.url;

  // En mode développement, si la requête concerne un de nos dossiers statiques,
  // on retourne une redirection vers l'URL du Blob.
  if (dev && (pathname.startsWith('/models/') || pathname.startsWith('/textures/') || pathname.startsWith('/assets/'))) {
    return new Response(null, {
      status: 307, // Temporary Redirect
      headers: {
        Location: `${BLOB_BASE_URL}${pathname}`
      }
    });
  }

  // Pour toutes les autres requêtes, on continue normalement.
  return resolve(event);
}
