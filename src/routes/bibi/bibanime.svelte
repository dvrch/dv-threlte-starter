<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import * as THREE from 'three';
	import { browser } from '$app/environment';
	import { getModelUrlByType } from '$lib/utils/geometry-loader';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';

	let {
		position = [0, 0, 0],
		rotation = [0, 0, 0],
		scale = 1
	}: {
		position?: [number, number, number];
		rotation?: [number, number, number];
		scale?: number | [number, number, number];
	} = $props();

	// Load the GLTF model dynamically
	let gltf: any = $state(null);
	let mixer: THREE.AnimationMixer | undefined = $state();

	onMount(async () => {
		if (browser) {
			try {
				// 1. Get initial URL from API mapping
				const initialUrl = await getModelUrlByType('bibigame');
				if (!initialUrl) return;

				// 2. Resolve to a working URL (local vs cloudinary)
				const workingUrl = await getWorkingAssetUrl(initialUrl, 'models');

				// 3. Load with Protection
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const loaded = await loader.loadAsync(workingUrl);

				// 🛡️ Fix the scene trees to prevent "visible of undefined" crash
				buildSceneGraph(loaded);

				gltf = loaded;

				if (gltf.animations && gltf.animations.length) {
					mixer = new THREE.AnimationMixer(gltf.scene);
					gltf.animations.forEach((clip: any) => {
						mixer?.clipAction(clip).play();
					});
				}
			} catch (err) {
				console.error('Failed to load bibi model safety:', err);
			}
		}
	});

	// Update the mixer on each frame
	useTask((delta: number) => {
		mixer?.update(delta);
	});
</script>

{#if browser && gltf}
	<T.Group {position} {rotation} {scale}>
		<T is={gltf.scene} />
	</T.Group>
{:else}
	<T.Group {position} {rotation} {scale} />
{/if}
