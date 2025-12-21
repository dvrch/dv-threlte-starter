import { dev } from '$app/environment';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
  // 🛡️ REDIRECTION BLOB DÉSACTIVÉE (Migration vers Cloudinary terminée)
  // Précédemment, on redirigeait /models/ et /textures/ vers Vercel Blob.
  // Maintenant, on laisse SvelteKit servir les fichiers locaux ou on laisse
  // le front-end décider de passer par Cloudinary via assetFallback.ts.

  return resolve(event);
}
