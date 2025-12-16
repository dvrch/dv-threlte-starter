<script lang="ts">
	import { writable } from 'svelte/store';
	import * as THREE from 'three';
	import { onMount } from 'svelte';
	import { T, useTask } from '@threlte/core';
	import { assets } from '$lib/services/assets';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';

	import { browser } from '$app/environment';

	// Store to manage texture state
	let currentTexture = writable(null);

	let model = $state<THREE.Group | null>(null); // To store the loaded 3D model
	let mixer = $state<THREE.AnimationMixer | null>(null); // For animations
	let clock = new THREE.Clock(); // To manage animation time

	// Path to your GLB model and textures
	const glbPath = getCloudinaryAssetUrl('cloth_sim_rffdfn.glb');
	const textures = [getCloudinaryAssetUrl('bibi.png')];
	let activeTextureIndex = 0;

	// Function to load a texture and update the material of the model
	export const nextTexture = async () => {
		const { TextureLoader } = await import('three');
		const { MeshStandardMaterial } = await import('three');
		const textureLoader = new TextureLoader();

		// Cycle texture index logic if we actually had multiple textures,
		// currently there's only one in the array but let's make it future-proof.
		// activeTextureIndex = (activeTextureIndex + 1) % textures.length;

		textureLoader.load(
			textures[activeTextureIndex],
			(texture) => {
				currentTexture.set(texture);
				if (model) {
					model.traverse((child) => {
						if ((child as any).isMesh) {
							(child as THREE.Mesh).material = new MeshStandardMaterial({ map: texture });
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

	onMount(() => {
		// Load the GLB model
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
					// Apply initial texture
					nextTexture();
				},
				undefined,
				(error) => {
					console.error('An error happened loading the GLB model:', error);
				}
			);
		};

		loadModel();

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
