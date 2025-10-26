<!-- AnimationController.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { useThrelte } from '@threlte/core';
  import * as THREE from 'three';

  export let mixer: THREE.AnimationMixer | null = null;
  export let model: THREE.Object3D | null = null;

  const { renderer, scene, camera } = useThrelte();
  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    if (mixer) mixer.update(clock.getDelta());
    if (model?.rotation) {
      model.rotation.y += 0.01;
    }
    renderer.render(scene, camera); //.current
  }

  onMount(() => {
    animate();
  });
</script>
