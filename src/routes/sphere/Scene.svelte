<script lang="ts">
	import { writable } from 'svelte/store';
	import * as THREE from 'three';
	import { onMount } from 'svelte'; // Added this import

	import { assets } from '$lib/services/assets';

	// Store to manage texture state
	let currentTexture = writable(null);
  
	// Path to your GLB model and textures
	const glbPath = assets.getUrl('/public/cloth_sim.glb'); // Corrected path for static asset
	const textures = [assets.getUrl('/public/bibi.png')];
	let activeTextureIndex = 0;
  
	let model = $state(null); // To store the loaded 3D model
	let mixer = $state(null); // For animations
	let clock = new THREE.Clock(); // To manage animation time
  
	onMount(() => {
		// Load the GLB model
		const loadModel = async () => {
			const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js');
			const loader = new GLTFLoader();
			loader.load(glbPath, (gltf) => {
				model = gltf.scene;
				if (gltf.animations.length > 0) {
					mixer = new THREE.AnimationMixer(model);
					const action = mixer.clipAction(gltf.animations[0]);
					action.play();
				}
			}, undefined, (error) => {
				console.error('An error happened loading the GLB model:', error);
			});
		};
	  
		// Function to load a texture and update the material of the model
		const changeTexture = async () => {
			const { TextureLoader } = await import('three');
			const { MeshStandardMaterial } = await import('three');
			const textureLoader = new TextureLoader();
			textureLoader.load(textures[activeTextureIndex], (texture) => {
				currentTexture.set(texture);
				if (model) {
					model.traverse((child) => {
						if (child.isMesh) {
							child.material = new MeshStandardMaterial({ map: texture });
						}
					});
				}
			}, undefined, (error) => {
				console.error('An error happened loading the texture:', error);
			});
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
