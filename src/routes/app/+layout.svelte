<script>
  import { Canvas } from '@threlte/core';
  import { T } from '@threlte/core';
  import { OrbitControls } from '@threlte/extras';
</script>

<Canvas
  shadows
  camera={{ position: [5, 2, 0], fov: 50 }}
  background="#f0f0f0"
>
  <!-- Caméra qui tourne automatiquement -->
  <T.PerspectiveCamera position={[5, 2, 0]} makeDefault>
    <OrbitControls
      enableDamping
      dampingFactor={0.05}
      autoRotate={true}
      autoRotateSpeed={1}
      maxPolarAngle={Math.PI / 2}
      minDistance={3}
      maxDistance={10}
    />
  </T.PerspectiveCamera>
  
  <!-- Lumières -->
  <T.AmbientLight intensity={0.5} />
  <T.DirectionalLight position={[5, 5, 5]} intensity={1} />
  
  <!-- Sphère principale -->
  <T.Mesh position={[0, 1, 0]}>
    <T.SphereGeometry args={[1, 32, 32]} />
    <T.MeshStandardMaterial color="#4a90e2" />
  </T.Mesh>
  
  <!-- Sol -->
  <T.Mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]}>
    <T.PlaneGeometry args={[10, 10]} />
    <T.MeshStandardMaterial color="#cccccc" />
  </T.Mesh>
</Canvas>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    overflow: hidden;
  }
</style>

