<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import * as THREE from 'three';

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

	// Load the GLTF model
	const gltfPromise = useGltf<THREE.Group>(assets.getUrl('/public/bibi.glb'));
	let gltf = $state();
	gltfPromise.then((res) => (gltf = res)).catch(err => {
		console.error('Failed to load bibi.glb', err);
	});

	// Create an animation mixer
	let mixer: THREE.AnimationMixer | undefined;

	// Play animations
	$effect(() => {
		if (gltf && gltf.animations && gltf.animations.length) {
			mixer = new THREE.AnimationMixer(gltf.scene);
			gltf.animations.forEach((clip) => {
				mixer?.clipAction(clip).play();
			});
		}
	});

	// Update the mixer on each frame
	useTask((_, delta) => {
		mixer?.update(delta);
	});
</script>

{#if gltf}
	<T.Group {position} {rotation} {scale}>
		<T is={gltf.scene} />
	</T.Group>
{/if}
