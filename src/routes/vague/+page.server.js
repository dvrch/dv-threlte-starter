// src/routes/vague/+page.server.js

import { env } from '$env/dynamic/public';

export async function load({ fetch }) {
	const PUBLIC_API_URL = env.PUBLIC_API_URL || '';

	try {
		// Si pas d'API_URL configurée, retourner un objet vide
		if (!PUBLIC_API_URL) {
			console.warn('PUBLIC_API_URL not configured for vague page');
			return {
				data: null,
				error: null
			};
		}

		// Pas besoin de fetch pour la page vague - c'est une page d'animation pure
		return {
			data: null,
			error: null
		};
	} catch (error) {
		const errorMessage = error instanceof Error ? error.message : 'Unknown error';
		console.error('Error loading vague page:', errorMessage);
		return {
			data: null,
			error: 'Failed to load page'
		};
	}
}
