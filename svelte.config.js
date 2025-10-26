import adapterAuto from '@sveltejs/adapter-auto';
import adapterStatic from '@sveltejs/adapter-static';
import preprocess from 'svelte-preprocess';

const isGhPages = process.env.DEPLOY_TARGET === 'GH_PAGES';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: preprocess(),
	kit: {
		adapter: isGhPages
			? adapterStatic({
					pages: 'build',
					assets: 'build',
					fallback: 'index.html',
					precompress: false,
					strict: true
			  })
			: adapterAuto(),
		paths: {
			base: isGhPages ? '/dv-threlte-starter' : ''
		}
	}
};

export default config;