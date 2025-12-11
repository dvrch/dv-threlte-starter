<script lang="ts">
	import { writable } from 'svelte/store';
	import * as THREE from 'three';
	import { onMount } from 'svelte';
	import { T, useTask } from '@threlte/core';
	import { browser } from '$app/environment';

	import { assets } from '$lib/services/assets';

	// Store to manage texture state
	let currentTexture = writable<any>(null);

	let model: THREE.Object3D | null = $state(null); // To store loaded 3D model
	let mixer: THREE.AnimationMixer | null = $state(null); // For animations
	let clock = new THREE.Clock(); // To manage animation time

	onMount(() => {
		// Path to your GLB model and textures
		const glbPath =
			'https://res.cloudinary.com/drcok7moc/raw/upload/v1765419051/dv-threlte/models/jaaezicvyjlywsw6lgwu.glb';
		const textures = [assets.getUrl('/public/bibi.png')];
		let activeTextureIndex = 0; // Moved inside onMount as it depends on textures

		// Load GLB model
		const loadModel = async () => {
			const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js');
			const loader = new GLTFLoader();
			loader.load(
				glbPath,
				(gltf) => {
					model = gltf.scene;
					if (gltf.animations.length > 0) {
						mixer = new THREE.AnimationMixer(model);
						const action = mixer.clipAction(gltf.animations[0]);
						action.play();
					}
				},
				undefined,
				(error) => {
					console.error('An error happened loading the GLB model:', error);
				}
			);
		};

		// Function to load a texture and update the material of the model
		const changeTexture = async () => {
			const { TextureLoader } = await import('three');
			const { MeshStandardMaterial } = await import('three');
			const textureLoader = new TextureLoader();
			textureLoader.load(
				textures[activeTextureIndex],
				(texture) => {
					currentTexture.set(texture);
					if (model) {
						model.traverse((child: any) => {
							if (child.isMesh) {
								child.material = new MeshStandardMaterial({ map: texture });
							}
						});
					}
				},
				undefined,
				(error) => {
					console.error('An error happened loading the texture:', error);
				}
			);
		};

		loadModel();
		changeTexture();

		useTask(() => {
			if (mixer) {
				const delta = clock.getDelta();
				mixer.update(delta);
			}
		});
	});
</script>

{#if browser}
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[5, 5, 5]} intensity={1} />
	{#if model}
		<T is={model} />
	{/if}
{:else}
	<!-- Placeholder for SSR if needed, or just render nothing -->
{/if}
