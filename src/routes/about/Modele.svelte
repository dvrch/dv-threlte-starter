
<script lang="ts">
  import { onMount } from 'svelte';
  import { T, Canvas } from '@threlte/core';
  import { Grid, OrbitControls } from '@threlte/extras';
  import * as THREE from 'three';
  // Remplacer useGltf et useGltfAnimations par GLTFLoader pour éviter l'erreur de module
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

  let {
    position = [0, 0, 0],
    rotation = [0, 0, 0]
  }: {
    position?: [number, number, number];
    rotation?: [number, number, number];
  } = $props();

  let clock = new THREE.Clock();
  let model: THREE.Object3D | null = null; // Déclarer le type pour éviter l'erreur implicite
  let mixer: THREE.AnimationMixer ; // Déclarer le type pour éviter l'erreur implicite

  // Charger le modèle GLTF
  const loader = new GLTFLoader();
  loader.load('/public/cloth_sim.glb', (gltf) => {
    model = gltf.scene;
    mixer = new THREE.AnimationMixer(model);
    gltf.animations.forEach((clip: THREE.AnimationClip) => mixer.clipAction(clip).play());
  });
	
	onMount(() => {
		function animate() {
			if (mixer) {
				mixer.update(clock.getDelta()); // Met à jour l'animation
			}
      if (model) {
        model.rotation.y += 0.00;
      }
      requestAnimationFrame(animate);
    }
    animate();
  });
</script>

<div class="scene-container">
  <Canvas>
    <T.PerspectiveCamera makeDefault position={[0, 5, 10]} fov={75}>
      <OrbitControls />
    </T.PerspectiveCamera>

    <T.PointLight intensity={0.2} position={[0, 4, 4]} color={0xFFFFFF} />
    <T.AmbientLight intensity={5.2} color={0x555555} />

    <T.Group {position} {rotation}>
      <T.MeshPhongMaterial shininess={10} />
      {#if model}
        <T is={model} />
      {/if}
    </T.Group>
  </Canvas>
</div>

<style>
  .scene-container {
    position: relative;
    width: 100%;
    height: 100vh;
  }
</style>



<!-- <script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import { Canvas, T } from '@threlte/core';
  import { OrbitControls } from '@threlte/extras';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

  // let { width = 400 } = $props();
  // let { height = 300 } = $props();
  let { position = [0, 0, 0] }: { position?: [number, number, number] } = $props();
  let { rotation = [0, 0, 0] }: { rotation?: [number, number, number] } = $props();


  let mixer: THREE.AnimationMixer;
  let clock = new THREE.Clock();
  const dispatch = createEventDispatcher();

  async function loadModel() {
    const gltfLoader = new GLTFLoader();
    const textureLoader = new THREE.TextureLoader();

    const [gltf, texture] = await Promise.all([
      gltfLoader.loadAsync('src/routes/planet/scene.gltf'), // Charge le modèle
      textureLoader.loadAsync('/public/zaki.png'), // Charge la texture
    ]);

    const mesh = gltf.scene.children[0] as THREE.Mesh;
    if (mesh.material) {
      mesh.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
    }

    mixer = new THREE.AnimationMixer(mesh);
    gltf.animations.forEach(clip => mixer.clipAction(clip).play());

    return gltf.scene;
  }

  onMount(async () => {
    const bibiScene = await loadModel();
    dispatch('sceneLoaded', { scene: bibiScene });
  });

  function animateScene() {
    const delta = clock.getDelta();
    mixer.update(delta);
  }
</script>
<div class="scene-container">
<Canvas >
  <T.PerspectiveCamera makeDefault position={[0, 1.5, 5]} fov={75} >
    <OrbitControls />
  </T.PerspectiveCamera>

  <T.AmbientLight intensity={0.6} />

  <T.Group {position} {rotation}>
    <T.Scene on:frame={animateScene}>
      <slot name="bibiScene" />
    </T.Scene>
  </T.Group>
</Canvas>
</div>

<style>
  .scene-container {
    width: 100%;
    height: 100vh;
    position: relative;
  }
</style>






<!-- <script lang="ts">
  import { GLTF, useGltfAnimations } from '@threlte/extras';

  // Charger les animations et le modèle GLTF
  const { actions, gltf } = useGltfAnimations();

  // Jouer toutes les animations une fois que le modèle est chargé et les actions sont disponibles
  $effect(() => {
    if (gltf && actions) {
    Object.values(actions).forEach(action => {
      if (action && typeof action.play === 'function') {
        action.play();
      }
    });
  }
  });
</script>

<GLTF bind:gltf={$gltf} url="/public/cloth_sim.glb" /> --> -->
