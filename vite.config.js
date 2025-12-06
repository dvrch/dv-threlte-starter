import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	build: {
		target: 'es2022'
	},
	plugins: [sveltekit()],
	ssr: {
		noExternal: ['three', 'troika-three-text', '@threlte/core', '@threlte/extras']
	},
	server: {
		proxy: {
			'/api': {
				target: 'http://localhost:8000',
				changeOrigin: true
			},
			'/admin': {
				target: 'http://localhost:8000',
				changeOrigin: true
			},
			'/health': {
				target: 'http://localhost:8000',
				changeOrigin: true
			}
		}
	}
};

export default config;
