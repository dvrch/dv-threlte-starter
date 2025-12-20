<script lang="ts">
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { Group } from 'three';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let { ref = $bindable(new Group()), ...rest } = $props();

	let gltfData = $state<any>(null);

	onMount(async () => {
		if (browser) {
			try {
				const url = await getWorkingAssetUrl('nissan2.glb', 'models');
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const rawGltf = await loader.loadAsync(url);
				buildSceneGraph(rawGltf); // 🛡️ Fixes all materials in-place
				gltfData = rawGltf;
			} catch (e) {
				console.error('Failed to load Nissan model:', e);
			}
		}
	});
</script>

<T is={ref} dispose={false} {...rest}>
	{#if gltfData}
		<T.Group scale={0.01}>
			<T is={gltfData.scene} />
		</T.Group>
	{/if}

	<slot {ref} />
</T>
