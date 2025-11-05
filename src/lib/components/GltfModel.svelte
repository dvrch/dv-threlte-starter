<script lang="ts">
  import { T } from '@threlte/core';
  import { useGltf } from '@threlte/extras';

  export let url: string;
  export let position: { x: number; y: number; z: number } = { x: 0, y: 0, z: 0 };
  export let rotation: { x: number; y: number; z: number } = { x: 0, y: 0, z: 0 };
  export let scale: number | { x: number; y: number; z: number } = 0.5; // Default scale to 0.5 as in the original component

</script>

{#await useGltf(url, { useDraco: true }) then gltf}
  <T 
    is={gltf.scene} 
    position={[position.x, position.y, position.z]}
    rotation={[rotation.x, rotation.y, rotation.z]}
    {scale}
  />
{:catch error}
  <!-- Fallback: Affiche une boîte rouge si le modèle ne peut pas être chargé -->
  <T.Mesh {position}>
    <T.BoxGeometry />
    <T.MeshStandardMaterial color="red" />
  </T.Mesh>
  {console.error(`Failed to load GLTF model from ${url}`, error)}
{/await}