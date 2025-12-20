<script lang="ts">
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let gltf = $state<any>(null);

	onMount(async () => {
		if (browser) {
			try {
				const url = await getWorkingAssetUrl('ghost.glb', 'models');
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());
				const loaded = await loader.loadAsync(url);
				buildSceneGraph(loaded);
				gltf = loaded;
			} catch (e) {
				console.error('Failed to load Ghost model in app folder', e);
			}
		}
	});
</script>

<T.Group>
	{#if gltf}
		<T is={gltf.scene} position={[0, 0, 0]} scale={1} rotation={[0, 0, 0]} />
	{/if}
</T.Group>
