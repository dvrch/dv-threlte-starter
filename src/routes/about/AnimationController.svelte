<!-- AnimationController.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { useThrelte } from '@threlte/core';
  import * as THREE from 'three';

  let { mixer = null }: { mixer?: THREE.AnimationMixer | null } = $props();
  let { model = null }: { model?: THREE.Object3D | null } = $props();

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
