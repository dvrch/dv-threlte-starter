// 🎯 Détection automatique de la plateforme de déploiement
const isGitHubPages = process.env.DEPLOY_TARGET === 'GH_PAGES';

// 📦 Import conditionnel de l'adapter
const adapter = isGitHubPages
	? (await import('@sveltejs/adapter-static')).default
	: (await import('@sveltejs/adapter-vercel')).default;

import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

// 🛣️ Chemin de base selon la plateforme
const basePath = isGitHubPages ? '/dv-threlte-starter' : '';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		paths: {
			base: basePath
		},
		// 🔄 Adapter dynamique selon la plateforme
		adapter: isGitHubPages
			? adapter({
				pages: 'build',
				assets: 'build',
				fallback: 'index.html',
				strict: false
			})
			: adapter({
				runtime: 'nodejs20.x'
			})
	},
	compilerOptions: {
		runes: true
	}
};

export default config;
