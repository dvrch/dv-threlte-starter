<script lang="ts">
	import { writable } from 'svelte/store';
	import * as THREE from 'three';
	import { onMount } from 'svelte';
	import { T, useTask } from '@threlte/core';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { browser } from '$app/environment';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	// Store to manage texture state
	let currentTexture = writable<THREE.Texture | null>(null);

	let model = $state<THREE.Group | null>(null); // To store the loaded 3D model
	let mixer = $state<THREE.AnimationMixer | null>(null); // For animations
	let clock = new THREE.Clock(); // To manage animation time

	let activeTextureIndex = 0;

	// Function to load a texture and update the material of the model
	export const nextTexture = async () => {
		const { TextureLoader } = await import('three');
		const { MeshStandardMaterial } = await import('three');
		const textureLoader = new TextureLoader();

		const texUrl = await getWorkingAssetUrl('zaki.png', 'textures');

		textureLoader.load(
			texUrl,
			(texture) => {
				currentTexture.set(texture);
				if (model) {
					model.traverse((child) => {
						if ((child as any).isMesh) {
							(child as THREE.Mesh).name = 'imageplane_cloth';
							(child as THREE.Mesh).material = new THREE.MeshBasicMaterial({
								map: texture,
								transparent: true,
								side: THREE.DoubleSide,
								toneMapped: false
							});
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

			try {
				const glbUrl = await getWorkingAssetUrl('cloth_sim.glb', 'models');
				loader.load(
					glbUrl,
					(gltf) => {
						buildSceneGraph(gltf);
						model = gltf.scene;
						if (gltf.animations.length > 0) {
							mixer = new THREE.AnimationMixer(model);
							const action = mixer.clipAction(gltf.animations[0]);
							action.play();
						}
						nextTexture();
					},
					undefined,
					(error) => {
						console.error('An error happened loading the GLB model:', error);
					}
				);
			} catch (e) {
				console.error('Failed to resolve URL for cloth sim:', e);
			}
		};

		const handleTexUpdate = async (e: any) => {
			const file = e.detail.file;
			if (!file || !/\.(jpg|jpeg|png|webp)$/i.test(file.name)) return;
			const { TextureLoader } = await import('three');
			const loader = new TextureLoader();
			const url = URL.createObjectURL(file);
			loader.load(url, (tex) => {
				currentTexture.set(tex);
				if (model) {
					model.traverse((child: any) => {
						if (child.isMesh) {
							child.material = new THREE.MeshBasicMaterial({
								map: tex,
								transparent: true,
								side: THREE.DoubleSide
							});
						}
					});
				}
			});
		};

		if (browser) {
			loadModel();
			window.addEventListener('directSceneUpload', handleTexUpdate);
		}

		useTask(() => {
			if (mixer) {
				const delta = clock.getDelta();
				mixer.update(delta);
			}
		});

		return () => {
			window.removeEventListener('directSceneUpload', handleTexUpdate);
		};
	});
</script>

{#if browser}
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[5, 5, 5]} intensity={1} />
	{#if model}
		<T is={model} />
	{/if}
{/if}
