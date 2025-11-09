<script lang="ts">
  import { useThrelte } from '@threlte/core';
  import { onMount } from 'svelte';
  import type { Object3D } from 'three';

  export let mixer: THREE.AnimationMixer;
  export let model: Object3D;

  const { renderer, scene, camera } = useThrelte();

  function animate() {
    requestAnimationFrame(animate);
    if (mixer) {
      mixer.update(0.016);
    }
    if (model?.rotation) {
      model.rotation.y += 0.01;
    }
    renderer.render(scene, camera.current);
  }

  onMount(() => {
    animate();
  });
</script>

<!-- 
<script lang="ts">
  import { writable } from 'svelte/store';
  import { T, Canvas, useThrelte } from '@threlte/core'; // Ajout de useThrelte
  import { OrbitControls, interactivity } from '@threlte/extras';
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { onMount } from 'svelte';
  import { navigate } from 'svelte-routing';
  import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry';
  import { FontLoader, Font } from 'three/examples/jsm/loaders/FontLoader.js';
  import { SvelteComponentTyped } from 'svelte';
  import Animation from './Animation.svelte';
  // Define ThreltePointerEvent type manually
  type ThreltePointerEvent = {
    object: THREE.Mesh;
    [key: string]: any;
  };

  const model = writable<THREE.Object3D>(new THREE.Object3D());
  let mixer: THREE.AnimationMixer;
  let font: Font | null = null;

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

      const loader = new FontLoader();
      font = await loader.loadAsync('/fonts/font.json');

      if (font) {
        model.set(gltf.scene);
      }
    } catch (error) {
      console.error('Erreur lors du chargement du modèle ou de la texture:', error);
    }
  });

  function handleClick() {
    navigate('/about/scene');
  }

  function createTextMesh(text: string, position: [number, number, number], size: number, color: string) {
    if (!font) {
      console.error("La police n'est pas encore chargée.");
      return null;
    }

    const geometry = new TextGeometry(text, {
      font: font,
      size: size,
      height: 0.01,
    });
    const material = new THREE.MeshPhongMaterial({ 
      color: color,
      emissive: new THREE.Color('#000000')
    });
    const textMesh = new THREE.Mesh(geometry, material);
    textMesh.position.set(...position);
    
    return textMesh;
  }

  function handlePointerEvent(e: ThreltePointerEvent) {
    const material = e.object.material as THREE.MeshPhongMaterial;
    if (material?.emissive) {
      material.emissive.set('#444444');
    }
  }

  function handlePointerLeave(e: ThreltePointerEvent) {
    const material = e.object.material as THREE.MeshPhongMaterial;
    if (material?.emissive) {
      material.emissive.set('#000000');
    }
  }

  function handleKeyPress(e: KeyboardEvent) {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }
</script>

<div class="scene-container">
  <Canvas>
    <Animation {mixer} model={$model} />
    <T.AmbientLight intensity={0.5} />
    <T.DirectionalLight position={[5, 10, 7.5]} intensity={1} />
    <T.PerspectiveCamera makeDefault position={[0, 1.5, 5]} fov={75}>
      <OrbitControls />
    </T.PerspectiveCamera>
    
    {#if $model && font}
      <T is={$model} />
      <interactivity.mesh 
        object={createTextMesh('Model Viewer', [0, 2, 0], 0.73, '#ffae00')}
        on:click={handleClick}
        on:keydown={handleKeyPress}
        on:pointerenter={handlePointerEvent}
        on:pointerleave={handlePointerLeave}
        role="button"
        tabindex="0"
      />
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
