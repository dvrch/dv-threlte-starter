<script lang="ts">
	import { onMount } from 'svelte';
	import { Canvas, useTask } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
	import { TextureLoader, MeshStandardMaterial } from 'three';
	import { OrbitControls } from '@threlte/extras';
	import { writable } from 'svelte/store';
	import * as THREE from 'three';
	import './styles.css';

	// Store to manage texture state
	let currentTexture = writable(null);
  
	// Path to your GLB model and textures
	const glbPath = '/public/cloth_sim.glb';
	const textures = ['/public/bibi.png'];
	let activeTextureIndex = 0;
  
	let model = null; // To store the loaded 3D model
	let mixer = null; // For animations
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
	  });
	};
  
	// Function to load a texture and update the material of the model
	const changeTexture = () => {
	  const textureLoader = new TextureLoader();
	  textureLoader.load(textures[activeTextureIndex], (texture) => {
		currentTexture.set(texture);
		model.traverse((child) => {
		  if (child.isMesh) {
			child.material = new MeshStandardMaterial({ map: texture });
		  }
		});
	  });
	};
  
	// Switch to the next texture
	const nextTexture = () => {
	  activeTextureIndex = (activeTextureIndex + 1) % textures.length;
	  changeTexture();
	};
  
	// Start loading the model when the component mounts
	onMount(() => {
	  loadModel();
	  changeTexture();
	});
  
	// Animate the model every frame
	useTask(() => {
	  if (mixer) {
		const delta = clock.getDelta();
		mixer.update(delta);
	  }
	});
</script>

<Canvas>
	<ambientLight intensity={0.5}></ambientLight>
	<directionalLight position={[5, 5, 5]} intensity={1}></directionalLight>
	{#if model}
	  <primitive object={model}></primitive>
	{/if}
	<OrbitControls></OrbitControls>
</Canvas>

<div class="controls">
	<button on:click={nextTexture}>Change Texture</button>
</div>

<style>
	.controls {
		position: absolute;
		top: 10px;
		left: 10px;
		z-index: 10;
	}
	button {
		padding: 10px;
		font-size: 16px;
	}
</style>
