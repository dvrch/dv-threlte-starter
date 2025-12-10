<script>
  import { T } from '@threlte/core';
  import { useGltf, useTexture } from '@threlte/extras';
  import { Group } from 'three';
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  // Runes syntax pour les props
  let { ref = new Group(), ...restProps } = $props();

  let gltf;
  let map;

  onMount(() => {
    if (browser) {
      gltf = useGltf('https://f001.backblazeb2.com/file/43dvcapp/models/spaceship.glb');
      map = useTexture('https://f001.backblazeb2.com/file/43dvcapp/textures/energy-beam-opacity.png');
    }
  });

  gltf?.then(() => {
    // Point d'extension si tu veux faire des ajustements sur les matériaux plus tard
  });
</script>

<T is={ref} dispose={false} {...restProps}>
  {#await gltf}
    loading
  {:then gltf}
    <T.Mesh is={gltf.scene} />
  {:catch error}
    <p>Error loading model</p>
  {/await}

  <slot {ref} />
</T>