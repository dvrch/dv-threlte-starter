<script lang="ts">
  import { T, useFrame } from '@threlte/core';
  import { useGltf } from '@threlte/extras';
  import * as THREE from 'three';

  export let position: [number, number, number] = [0, 0, 0];
  export let rotation: [number, number, number] = [0, 0, 0];
  export let scale: number | [number, number, number] = 1;

  // Load the GLTF model
  const gltf = useGltf<THREE.Group>('/public/bibi.glb');

  // Create an animation mixer
  let mixer: THREE.AnimationMixer | undefined;

  // Play animations
  $: if ($gltf && $gltf.animations.length) {
    mixer = new THREE.AnimationMixer($gltf.scene);
    $gltf.animations.forEach(clip => {
      mixer?.clipAction(clip).play();
    });
  }

  // Update the mixer on each frame
  useFrame((_, delta) => {
    mixer?.update(delta);
  });

</script>

{#if $gltf}
  <T.Group {position} {rotation} {scale}>
    <T is={$gltf.scene} />
  </T.Group>
{/if}