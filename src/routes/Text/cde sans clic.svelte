<script lang="ts">
  import { Canvas } from '@threlte/core';
  import { T } from '@threlte/core';
  import { OrbitControls } from '@threlte/extras';
  import { writable } from 'svelte/store';

  const color = writable(0x44ffff);
</script>

<div class="scene-container">
  <Canvas renderMode="always">
    <!-- Caméra -->
    <T.PerspectiveCamera 
      position={[0, 2, 5]} 
      fov={75}
      makeDefault
    >
      <OrbitControls enableDamping />
    </T.PerspectiveCamera>

    <!-- Lumières -->
    <T.AmbientLight intensity={0.5} />
    <T.DirectionalLight 
      position={[5, 5, 5]} 
      intensity={1} 
      castShadow
    />

    <!-- Cube -->
    <T.Mesh 
      position={[0, 0, 0]}
      on:pointerdown={() => {
        $color = Math.floor(Math.random() * 16777215);
      }}
      let:ref
    >
      <T.BoxGeometry args={[1, 1, 1]} />
      <T.MeshStandardMaterial color={$color} />
    </T.Mesh>
  </Canvas>
</div>

<style>
  .scene-container {
    width: 100%;
    height: 100vh;
    background: #000;
  }
</style>