<script lang="ts">
	import { Group } from 'three';
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfGarden = $state<any>(null);

	onMount(async () => {
		if (browser) {
			try {
				const resolved = await getWorkingAssetUrl('garden1.glb', 'models');
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());
				const rawGltf = await loader.loadAsync(resolved);
				const { nodes, materials } = buildSceneGraph(rawGltf);
				gltfGarden = { ...rawGltf, nodes, materials };
			} catch (e) {
				console.error('Failed to load lib garden model:', e);
			}
		}
	});
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltfGarden}
		<T.Group scale={0.01}>
			<T is={gltfGarden.scene} />
		</T.Group>
	{/if}

	<slot {ref} />
</T>
