<script lang="ts">
  import { T, useTask } from '@threlte/core';
  import { useGltf } from '@threlte/extras';
  import * as THREE from 'three';

  let { position = [0, 0, 0] }: { position?: [number, number, number] } = $props();
  let { rotation = [0, 0, 0] }: { rotation?: [number, number, number] } = $props();
  let { scale = 1 }: { scale?: number | [number, number, number] } = $props();

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
  useTask((_, delta) => {
    mixer?.update(delta);
  });

</script>

{#if $gltf}
  <T.Group {position} {rotation} {scale}>
    <T is={$gltf.scene} />
  </T.Group>
{/if}