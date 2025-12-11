<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import * as THREE from 'three';
	import { browser } from '$app/environment';

	let {
		position = [0, 0, 0],
		rotation = [0, 0, 0],
		scale = 1
	}: {
		position?: [number, number, number];
		rotation?: [number, number, number];
		scale?: number | [number, number, number];
	} = $props();

	import { assets } from '$lib/services/assets';

	// Use the useGltf hook to load the model
	let gltf: any = $state(null);
	let mixer: THREE.AnimationMixer | undefined;

	$effect(() => {
		if (browser) {
			const gltfStore = useGltf(
				'https://res.cloudinary.com/drcok7moc/raw/upload/v1765419051/dv-threlte/models/jaaezicvyjlywsw6lgwu.glb'
			);
			gltfStore
				.then((loaded) => {
					gltf = loaded;
					// Set up animation mixer when model is loaded
					if (loaded && loaded.animations && loaded.animations.length > 0) {
						mixer = new THREE.AnimationMixer(loaded.scene);
						loaded.animations.forEach((clip: THREE.AnimationClip) => {
							mixer?.clipAction(clip).play();
						});
					}
				})
				.catch((err) => {
					console.error('Failed to load 3D model from Cloudinary', err);
					gltf = null;
				});
		}
	});

	// Animate model using useTask
	useTask((delta) => {
		if (!mixer) return;
		mixer.update(delta);
	});
</script>

{#if browser && gltf}
	<T.Group {position} {rotation} {scale}>
		<T is={gltf.scene} />
	</T.Group>
{/if}
