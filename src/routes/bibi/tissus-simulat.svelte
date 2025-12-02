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

  // Use the useGltf hook to load the model
  const gltf = useGltf<THREE.Group>('/public/cloth_sim.glb');
  let $gltf = $derived(gltf);

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
    //   $gltf.scene.traverse((child) => {
    //     if (child instanceof THREE.Mesh) {
    //       child.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
    //     }
    //   });
    // });
  }
</script>

{#if $gltf}
  <T.Group {position} {rotation} {scale}>
    <T is={$gltf.scene} />
  </T.Group>
{/if}