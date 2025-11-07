<script>
  import { AddEquation, CustomBlending, Group, LessEqualDepth, OneFactor } from 'three';
  import { T } from '@threlte/core';
  import { useGltf } from '@threlte/extras';
  import { useTexture } from '@threlte/extras';
  import Nissan from '../Nissan.svelte';
    import Bloom from '../bloom.svelte';

  export const ref = new Group();

  const gltf = useGltf('/models/spaceship.glb');

  const texture = useTexture('/textures/energy-beam-opacity.png');

  gltf.then((gltf) => {
    const cubeNode = gltf.nodes.Cube;
    if (cubeNode && cubeNode.material) {
      cubeNode.material.blending = CustomBlending;
      cubeNode.material.blendEquation = AddEquation;
      cubeNode.material.blendSrc = OneFactor;
      cubeNode.material.blendDst = OneFactor;
      cubeNode.material.depthWrite = false;
      cubeNode.material.depthTest = false;
      cubeNode.material.map = texture;
    } else {
      console.warn("gltf.nodes.Cube or its material is undefined in spaceship.svelte");
    }
  });

  
</script>

<T is={ref} dispose={false} {...$$restProps}>
  {#await gltf}
    <slot name="fallback" />
  {:then gltf}
    <T.Group scale={0.003} rotation={[0, -Math.PI * 0.5, 0]} position={[0.95, 0, -2.235]}>
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube001_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[739.26, -64.81, 64.77]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cylinder002_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[739.69, -59.39, -553.38]}
        rotation={[Math.PI / 2, 0, 0]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cylinder003_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[742.15, -64.53, -508.88]}
        rotation={[Math.PI / 2, 0, 0]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube003_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[737.62, 46.84, -176.41]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cylinder004_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[789.52, 59.45, -224.91]}
        rotation={[1, 0, 0]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube001_RExtr001_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[745.54, 159.32, -5.92]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube001_RPanel003_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[739.26, 0, 0]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube001_RPanel003_RExtr_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[739.26, 0, 0]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube002_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[736.79, -267.14, -33.21]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube001_RPanel001_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[739.26, 0, 0]}
      />
      <T.Mesh
        castShadow
        receiveShadow
        geometry={gltf.nodes.Cube001_RPanel003_RExtr001_spaceship_racer_0.geometry}
        material={gltf.materials.spaceship_racer}
        position={[739.26, 0, 0]}
      />
      <T.Mesh
        geometry={gltf.nodes.Cube005_cockpit_0.geometry}
        material={gltf.materials.cockpit}
        position={[739.45, 110.44, 307.18]}
        rotation={[0.09, 0, 0]}
      />
      <T.Mesh
        geometry={gltf.nodes.Sphere_cockpit_0.geometry}
        material={gltf.materials.cockpit}
        position={[739.37, 145.69, 315.6]}
        rotation={[0.17, 0, 0]}
      />
      {#await texture then mapValue}
        <T.Mesh position={[740, -60, -1350]} rotation.x={Math.PI * 0.5}>
          <T.CylinderGeometry args={[70, 25, 1600, 15]} />
          <T.MeshBasicMaterial
            color={[1.0, 0.4, 0.02]}
            alphaMap={mapValue}
            transparent
            blending={CustomBlending}
            blendDst={OneFactor}
            blendEquation={AddEquation}
          />
        </T.Mesh>
      {/await}
    </T.Group>
  {:catch error}
    <slot name="error" {error} />
  {/await}

  <slot {ref} />
</T>