<script lang="ts">
	import { Group } from 'three';
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let { ref = $bindable(new Group()), ...rest } = $props();

	let gltfGhostValue = $state(null);

	onMount(async () => {
		if (browser) {
			try {
				const resolved = await getWorkingAssetUrl('ghost.glb', 'models');
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());
				const raw = await loader.loadAsync(resolved);
				buildSceneGraph(raw);
				gltfGhostValue = raw;
			} catch (e) {
				console.error('Failed to load Ghost model in spaceship route', e);
			}
		}
	});
</script>

<T is={ref} dispose={false} {...rest}>
	{#if gltfGhostValue}
		<T.Mesh
			geometry={gltfGhostValue.nodes.Ghost002.geometry}
			material={gltfGhostValue.materials.Outline}
		/>
	{/if}

	<slot {ref} />
</T>
