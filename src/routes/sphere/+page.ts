// src/routes/sphere/+page.ts

/**
 * This tells SvelteKit not to prerender this page at build time.
 * Because this page fetches dynamic data from the backend API,
 * it needs to be rendered on the server at request time.
 */
export const prerender = false;