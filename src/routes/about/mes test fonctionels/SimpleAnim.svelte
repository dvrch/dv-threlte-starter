<script lang="ts">
  import { writable } from 'svelte/store';
  import { T, Canvas } from '@threlte/core';
  import { OrbitControls, Text } from '@threlte/extras';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { onMount } from 'svelte';
  import { navigate } from 'svelte-routing';
  import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry';

  const clock = new THREE.Clock();
  const model = writable<THREE.Object3D | null>(null);
  let mixer: THREE.AnimationMixer;

  onMount(async () => {
    try {
      const gltf = await new GLTFLoader().loadAsync('/public/cloth_sim.glb');
      const texture = await new THREE.TextureLoader().loadAsync('/public/zaki.png');

      const mesh = gltf.scene.children[0] as THREE.Mesh;
      if (mesh.material) {
        mesh.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
      }

      mixer = new THREE.AnimationMixer(gltf.scene);
      gltf.animations.forEach((clip) => mixer.clipAction(clip).play());

      animate();
      model.set(gltf.scene);
    } catch (error) {
      console.error('Error loading model or texture:', error);
    }
  });

  function animate() {
    mixer?.update(clock.getDelta());
    if ($model?.rotation ) {
    $model.rotation.y += 0.0; // Apply rotation directly
    };
    requestAnimationFrame(animate);
  }

  function handleClick() {
    navigate('/about/scene');
  }
</script>

<div class="scene-container">
  <Canvas>
    <h1>Model Viewer</h1>
    <p>This is a simple model viewer that loads a 3D model and a texture.</p>
    <T.AmbientLight intensity={0.5} />
    <T.DirectionalLight position={[5, 10, 7.5]} intensity={1} />
    <T.PerspectiveCamera makeDefault position={[0, 1.5, 5]} fov={75}>
      <OrbitControls />
    </T.PerspectiveCamera>
    {#if $model}
    <T is={$model} rotation? />
    {/if}
    <T.Text
      position={[0, 2, 0]} 
      fontSize={0.3}
      color="#ffae00"
      on:click={handleClick}
      onClick={() => console.log('Clicked!')}
    >
      Model Viewer
    </T.Text>

    <T.Text
      position={[0, 1.5, 0]} 
      fontSize={0.15}
      color="#ffffff"
    >
      This is a simple model viewer that loads a 3D model and a texture.
    </T.Text>
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
  import { writable } from 'svelte/store';
  import { T, Canvas } from '@threlte/core';
  import { OrbitControls } from '@threlte/extras';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { onMount } from 'svelte';

  const clock = new THREE.Clock();
  const model = writable<THREE.Object3D | null>(null);
  let mixer: THREE.AnimationMixer;

  onMount(async () => {
    try {
      const gltf = await new GLTFLoader().loadAsync('/public/cloth_sim.glb');
      const texture = await new THREE.TextureLoader().loadAsync('/public/zaki.png');

      const mesh = gltf.scene.children[0] as THREE.Mesh;
      if (mesh.material) {
        mesh.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
      }

      mixer = new THREE.AnimationMixer(gltf.scene);
      gltf.animations.forEach((clip) => mixer.clipAction(clip).play());

      animate();
      model.set(gltf.scene);
    } catch (error) {
      console.error('Error loading model or texture:', error);
    }
  });

  function animate() {
    mixer?.update(clock.getDelta());
    if ($model?.rotation ) {
    $model.rotation.y += 0.0; // Apply rotation directly
    };
    requestAnimationFrame(animate);
  }
</script>


<div class="scene-container">
  <Canvas>
    <h1>Model Viewer</h1>
    <p>This is a simple model viewer that loads a 3D model and a texture.</p>
    <T.AmbientLight intensity={0.5} />
    <T.DirectionalLight position={[5, 10, 7.5]} intensity={1} />
    <T.PerspectiveCamera makeDefault position={[0, 1.5, 5]} fov={75}>
      <OrbitControls />
    </T.PerspectiveCamera>
  {#if $model}
    <T is={$model} rotation? />
    {/if}
  </Canvas>
</div> -->



  
<!-- <div class="scene-container">
  <Canvas>
    <T.PerspectiveCamera makeDefault position={[0, 5, 10]} fov={75}>
      <OrbitControls />
    </T.PerspectiveCamera>

    <T.PointLight intensity={0.2} position={[0, 4, 4]} />
    <T.AmbientLight intensity={5.2} />

    {#if $model}
      <T is={$model} rotation? />
    {/if}
  </Canvas>
</div>



<style>
  .scene-container {
    position: relative;
    width: 100%;
    height: 100vh;
  }
</style> -->



<!-- <script lang="ts">
  import { T, Canvas } from '@threlte/core';
  import { Grid, OrbitControls } from '@threlte/extras';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { TextureLoader } from 'three';
  import { onMount } from 'svelte';
  export const width = 100;
  export const height = 100;
  export let position: [number, number, number] = [0, 0, 0];
  export let rotation: [number, number, number] = [0, 0, 0];

  let clock = new THREE.Clock();
  let model: THREE.Object3D | null = null;
  let mixer: THREE.AnimationMixer;
  let texture: THREE.Texture;

  // Fonction pour charger la texture et le modèle
  const textureLoader = new TextureLoader();
  texture = textureLoader.load('/public/zaki.png');
  function init() {
    loadModel();
  }

  // Nouvelle fonction utilitaire pour appliquer la texture
  function applyTextureToMaterial(material: THREE.Material) {
    if (material instanceof THREE.MeshStandardMaterial) {
      material.map = texture;
      material.needsUpdate = true;
    }
  }

  // Nouvelle fonction pour traiter le maillage
  function processMesh(mesh: THREE.Mesh) { //comentaire: on a changé le type de mesh de THREE.Object3D à THREE.Mesh
    if (mesh.isMesh) {
      const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
      materials.forEach(applyTextureToMaterial);
    }
  }

  // Nouvelle fonction pour charger le modèle GLTF
  function loadModel() {
    const loader = new GLTFLoader();
    loader.load('/public/cloth_sim.glb', (gltf) => {
      model = gltf.scene;
      mixer = new THREE.AnimationMixer(model);
      gltf.animations.forEach((clip: THREE.AnimationClip) => mixer.clipAction(clip).play());

      model.traverse((child) => {
        processMesh(child as THREE.Mesh);
      });

      // Démarrer l'animation uniquement dans le navigateur
      onMount(animate);
      // if (typeof window !== 'undefined') {animate();}

    });
  }

  // Fonction d'animation
  function animate() { 
    if (mixer) { 
      mixer.update(clock.getDelta()); // Met à jour l'animation
    }
    if (model) { 
      model.rotation.y += 0.001; 
    }
    requestAnimationFrame(animate); // Appel de la fonction d'animation
  }

  // Appeler la fonction d'initialisation uniquement dans le navigateur
  onMount(init);
  // if (typeof window!== 'undefined') {init(); }

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
        <T is={mixer} />
      {/if}
      <gltf.scene />
    </T.Group>
  </Canvas>
</div>


<!-- $--------------------$ -->
<!-- <script lang="ts">
  import { Canvas, T } from '@threlte/core';
  import { GLTF, useGltfAnimations } from '@threlte/extras';
  import { OrbitControls } from '@threlte/extras';

  const { actions, gltf } = useGltfAnimations();
  $: if (gltf) {
			Object.values($actions).forEach(action => action?.play());
		}
</script>

<div class="scene-container">
  <Canvas>
    <T.PerspectiveCamera makeDefault position={[0, 1.5, 5]} fov={75}>
      <OrbitControls />
    </T.PerspectiveCamera>
    <T.AmbientLight intensity={0.6} />

    <GLTF bind:gltf={$gltf} url="/public/cloth_sim.glb" />
  </Canvas>
</div>

<style>
  .scene-container {
    position: relative;
    width: 100%;
    height: 100vh;
  }
</style> -->
