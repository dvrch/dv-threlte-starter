<script lang="ts">
	import { T } from '@threlte/core';
	import { Group, LessEqualDepth, TextureLoader } from 'three';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { createDracoLoader } from '$lib/utils/draco-loader';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfResultData = $state<any>(null);
	let mapResultData = $state<any>(null);
	let isLoading = $state(true);

	onMount(async () => {
		if (browser) {
			try {
				const gltfUrl = await getWorkingAssetUrl('spaceship.glb', 'models');
				const mapUrl = await getWorkingAssetUrl('energy-beam-opacity.png', 'textures');

				// Load GLTF manually to avoid lifecycle hook issues with async URLs
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const rawGltf = await loader.loadAsync(gltfUrl);

				// Apply alpha fix
				function alphaFix(material: any) {
					if (!material) return;
					material.transparent = true;
					material.alphaToCoverage = true;
					material.depthFunc = LessEqualDepth;
					material.depthTest = true;
					material.depthWrite = true;
				}
				if (rawGltf.materials.spaceship_racer) alphaFix(rawGltf.materials.spaceship_racer);
				if (rawGltf.materials.cockpit) alphaFix(rawGltf.materials.cockpit);

				gltfResultData = rawGltf;

				// Load Texture manually
				const texLoader = new TextureLoader();
				mapResultData = await texLoader.loadAsync(mapUrl);
			} catch (e) {
				console.error('Failed to load spaceship assets:', e);
			} finally {
				isLoading = false;
			}
		}
	});
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltfResultData}
		<T.Group scale={0.01}>
			<T is={gltfResultData.scene} />
		</T.Group>

		{#if mapResultData}
			<T.Mesh position={[0, -0.6, -13.5]} rotation.x={Math.PI * 0.5} scale={100}>
				<T.CylinderGeometry args={[0.7, 0.25, 16, 15]} />
				<T.MeshBasicMaterial color="#ff6605" alphaMap={mapResultData} transparent />
			</T.Mesh>
		{/if}
	{:else if isLoading}
		<slot name="fallback" />
	{/if}

	<slot {ref} />
</T>
