<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import * as THREE from 'three';
	import { browser } from '$app/environment';
	import { getModelUrlByType } from '$lib/utils/geometry-loader';

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
	let modelUrl = $state<string | null>(null);
	let gltf: any = $state(null);

	// Find the model URL from API
	getModelUrlByType('bibigame').then((url) => {
		modelUrl = url;
	});

	

	// Load the GLTF model when URL is available
	$effect(() => {
		if (browser && modelUrl) {
			const gltfStore = useGltf(modelUrl
			gltfStore
				.then((loaded) => {
					gltf = loaded;
				})
				.catch((err) => {
					console.error('Failed to load bibi model:', err);
					gltf = null;
				});
		}
	});

	// Create an animation mixer
	let mixer: THREE.AnimationMixer | undefined;

	// Play animations
	$effect(() => {
		if (gltf && gltf.animations && gltf.animations.length) {
			mixer = new THREE.AnimationMixer(gltf.scene);
			gltf.animations.forEach((clip: any) => {
				mixer?.clipAction(clip).play();
			});
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
	<!-- Fallback for SSR -->
	<T.Group {position} {rotation} {scale} />
{/if}
