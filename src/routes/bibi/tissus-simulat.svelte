<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import * as THREE from 'three';
	import { AssetManager } from '$lib/config';

	let {
		position = [0, 0, 0],
		rotation = [0, 0, 0],
		scale = 1
	}: {
		position?: [number, number, number];
		rotation?: [number, number, number];
		scale?: number | [number, number, number];
	} = $props();

	// Use the useGltf hook to load the model
	const gltf = useGltf(AssetManager.getAssetUrl('public/cloth_sim.glb'));

	// Animate the model using useTask
	let mixer: THREE.AnimationMixer | undefined;
	useTask((delta: number) => {
		if (!mixer) return;
		mixer.update(delta);
	});

	// When the model is loaded, set up the animation mixer
	$effect(() => {
		if (gltf) {
			gltf
				.then((loadedGltf) => {
					mixer = new THREE.AnimationMixer(loadedGltf.scene);
					loadedGltf.animations.forEach((clip: any) => {
						mixer?.clipAction(clip).play();
					});
				})
				.catch((err: any) => console.error('Failed to load cloth_sim.glb', err));
		}
	});

	// Optional: Apply a texture if needed, assuming the model has a mesh
	// const textureLoader = new THREE.TextureLoader();
	// textureLoader.load('/public/zaki.png', (texture) => {
	//   gltf.scene.traverse((child) => {
	//     if (child instanceof THREE.Mesh) {
	//       child.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
	//     }
	//   });
	// });
</script>

{#await gltf then loadedGltf}
	<T.Group {position} {rotation} {scale}>
		<T is={loadedGltf.scene} />
	</T.Group>
{/await}
