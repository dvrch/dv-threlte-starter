<script>
	import { Group } from 'three';
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfThrelteData = $state(null);

	onMount(async () => {
		if (browser) {
			try {
				const resolved = await getWorkingAssetUrl('threlte.glb', 'models');
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());
				const raw = await loader.loadAsync(resolved);
				buildSceneGraph(raw);
				gltfThrelteData = raw;
			} catch (e) {
				console.error('Failed to load Threlte logo model in spaceship route', e);
			}
		}
	});
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltfThrelteData}
		<T.Mesh
			geometry={gltfThrelteData.nodes.Cube.geometry}
			material={gltfThrelteData.materials.Material}
			position={[0, 1, 2]}
		/>
	{/if}

	<slot {ref} />
</T>
