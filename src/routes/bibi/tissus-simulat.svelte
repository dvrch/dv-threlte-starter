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
	import { dracoLoader } from '$lib/utils/draco';

	const CLOUDINARY_BASE_URL = 'https://res.cloudinary.com/drcok7moc/raw/upload';
	const CLOTH_SIM_GLB_URL = `${CLOUDINARY_BASE_URL}/public/cloth_sim.glb`;

	// This component should be loaded dynamically via the database
	// The cloth_sim model is available as geometry ID 71 in the database
	console.warn('This component should be loaded via Dynamic3DModel with geometry ID 71');
	const gltf = useGltf<THREE.Group>(CLOTH_SIM_GLB_URL, { dracoLoader });
	gltf.catch((err) => console.error('Failed to load cloth_sim.glb - use database instead', err));

	// Animate the model using useTask
	let mixer: THREE.AnimationMixer | undefined;
	useTask((_, delta) => {
		if (!mixer) return;
		mixer.update(delta);
	});

	// When the model is loaded, set up the animation mixer
	$effect(() => {
		if (gltf) {
			mixer = new THREE.AnimationMixer(gltf.scene);
			gltf.animations.forEach((clip) => {
				mixer?.clipAction(clip).play();
			});
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

{#if gltf}
	<T.Group {position} {rotation} {scale}>
		<T is={gltf.scene} />
	</T.Group>
{/if}
