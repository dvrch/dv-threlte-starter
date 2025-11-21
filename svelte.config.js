import adapterAuto from '@sveltejs/adapter-auto';
import adapterStatic from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const isGhPages = process.env.DEPLOY_TARGET === 'GH_PAGES';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapterStatic({
					pages: 'build',
					assets: 'build',
					fallback: 'index.html',
					precompress: false,
					strict: true
			  }),
		paths: {
			base: isGhPages ? '/dv-threlte-starter' : ''
		},
		prerender: {
			handleHttpError: ({ path, referrer, message }) => {
				// Ignore 500 errors for 3D pages during prerendering
				if (path.includes('/desksc') || path.includes('/sphere') || path.includes('/vague')) {
					return;
				}
				throw new Error(message);
			}
		}
	},
	compilerOptions: {
		runes: true
	}
};

export default config;