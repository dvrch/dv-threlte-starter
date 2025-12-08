<script lang="ts">
	import { useTask, T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
	import { TextureLoader, MeshStandardMaterial } from 'three';
	import { OrbitControls } from '@threlte/extras';
	import { writable } from 'svelte/store';
	import * as THREE from 'three';

	import { assets } from '$lib/services/assets';

	// Store to manage texture state
	let currentTexture = writable(null);
  
	// Path to your GLB model and textures
	const glbPath = assets.getUrl('/public/cloth_sim.glb');
	const textures = [assets.getUrl('/public/bibi.png')];
	let activeTextureIndex = 0;
  
	let model = $state(null); // To store the loaded 3D model
	let mixer = $state(null); // For animations
	let clock = new THREE.Clock(); // To manage animation time
  
	// Load the GLB model
	const loadModel = () => {
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
	const changeTexture = () => {
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
  
	// Switch to the next texture
	export const nextTexture = () => {
	  activeTextureIndex = (activeTextureIndex + 1) % textures.length;
	  changeTexture();
	};
  
	loadModel();
	changeTexture();
  
	// Animate the model every frame
	useTask(() => {
	  if (mixer) {
		const delta = clock.getDelta();
		mixer.update(delta);
	  }
	});
</script>

<T.PerspectiveCamera makeDefault position={[0, 5, 10]} fov={75}>
    <OrbitControls />
</T.PerspectiveCamera>

<T.AmbientLight intensity={0.5} />
<T.DirectionalLight position={[5, 5, 5]} intensity={1} />
{#if model}
    <T is={model} />
{/if}
