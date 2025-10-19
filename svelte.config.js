import adapter from '@sveltejs/adapter-static'; // MODIFIÉ
import preprocess from 'svelte-preprocess';
import seqPreprocessor from 'svelte-sequential-preprocessor';
import { preprocessThrelte } from '@threlte/preprocess';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    preprocess: seqPreprocessor([preprocess(), preprocessThrelte()]),
    kit: {
        adapter: adapter({
            // default options are fine
            pages: 'build',
            assets: 'build',
            fallback: undefined,
            precompress: false,
            strict: true
        })
    }
};

export default config;
