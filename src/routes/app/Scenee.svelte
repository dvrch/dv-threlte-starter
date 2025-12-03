<script lang="ts">
	import Bibigame from './bibigame.svelte';
  import { onMount, onDestroy } from 'svelte';
  import { writable } from 'svelte/store';
  import Nissangame from './nissangame.svelte';
  //import Garden from './models/garden.svelte'; // Temporarily disabled - 404 on GLB file
  import { T } from '@threlte/core';
  import { ContactShadows, Float, Grid, OrbitControls, useGltf } from '@threlte/extras';
  import Bloom from './models/bloom.svelte';
  //import Nissan from './models/Nissan.svelte'; // Temporarily disabled - restProps error
  import AddGeometry from './AddGeometry.svelte';
  import { addToast } from '$lib/stores/toasts';
  import GltfModel from '$lib/components/GltfModel.svelte'; // Importer le nouveau composant

  import Tissus from '../bibi/tissus-simulat.svelte';
  import Bibanime from '../bibi/bibanime.svelte';
  import Vague from '../vague/+page.svelte';
  import Spaceship from '../Spaceship/+page.svelte';
  import Desk from '../desksc/+page.svelte';
  
  // ✅ Importer les variables d'environnement
  import { PUBLIC_API_URL } from '$env/static/public';
  
  type Position = {
    x: number;
    y: number;
    z: number;
  };

  type Geometry = {
    id: string;
    position: Position;
    rotation: Position;
    type: string;
    color: string;
    name: string;
    model_url?: string; // Rendre model_url optionnel
  };

  let geometries: Geometry[] = [];

  const selectedGeometry = writable<Geometry | null>(null);

  const handleGeometryClick = (geometry: Geometry) => {
    $selectedGeometry = geometry;
  };

  const deleteGeometry = async (id: string) => {
    try {
      const response = await fetch(`/api/geometries/${id}/`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete geometry');
      loadGeometries();
      addToast('Geometry deleted successfully!', 'success');
    } catch (error) {
      console.error('Error deleting geometry:', error);
      addToast('Failed to delete geometry. Please try again.', 'error');
    }
  };

  const loadGeometries = async () => {
    try {
      // ✅ Utiliser PUBLIC_API_URL au lieu de localhost:8000
      const apiUrl = PUBLIC_API_URL 
        ? `${PUBLIC_API_URL}/api/geometries/` 
        : '/api/geometries/';
      
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error('Failed to fetch geometries');
      const data = await response.json();
      geometries = data.results || [];
      console.log('Loaded geometries:', geometries);
    } catch (error) {
      console.error('Error loading geometries:', error);
    }
  };

  onMount(() => {
    loadGeometries();
    window.addEventListener('modelAdded', loadGeometries);
  });

  onDestroy(() => {
    window.removeEventListener('modelAdded', loadGeometries);
  });

  const handleGeometryChange = () => {
    loadGeometries();
    $selectedGeometry = null;
  };
</script>  

<T.PerspectiveCamera makeDefault position={[-10, 10, 10]} fov={70} aspect={window.innerWidth * 0.3 / window.innerHeight * 0.3}>
  <OrbitControls autoRotate enableZoom={true} minDistance={0} maxDistance={80} target={[0, 1.5, 0]} />
</T.PerspectiveCamera>

<T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
<T.AmbientLight intensity={0.2} />

<Grid position={[0, -0.001, 0]} cellColor="#ffffff" sectionColor="#ffffff" sectionThickness={0} fadeDistance={25} cellSize={2} />

<ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />

<Bloom />

<AddGeometry 
  selectedGeometry={$selectedGeometry} 
  on:geometryChanged={handleGeometryChange} 
/>

{#each geometries as geometry (geometry.id)}
  <Float 
    floatIntensity={1} 
    floatingRange={[0, 1]} 
    on:click={() => handleGeometryClick(geometry)}
  >
    {#if geometry.model_url}
      <GltfModel url={geometry.model_url} position={geometry.position} rotation={geometry.rotation} />
    {:else if geometry.type === 'box'}
      <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
      rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
        <T.BoxGeometry />
        <T.MeshStandardMaterial color={geometry.color} />
      </T.Mesh>
    {:else if geometry.type === 'torus'}
      <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
      rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
        <T.TorusKnotGeometry args={[0.5, 0.15, 100, 12, 2, 3]} />
        <T.MeshStandardMaterial color={geometry.color} />
      </T.Mesh>
    {:else if geometry.type === 'icosahedron'}
      <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
      rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
        <T.IcosahedronGeometry />
        <T.MeshStandardMaterial color={geometry.color} />
      </T.Mesh>
    {:else if geometry.type === 'nissangame'}
      <Nissangame />
    {:else if geometry.type === 'garden'}
      <!-- Garden temporarily disabled -->
    {:else if geometry.type === 'nissan'}
      <!-- Nissan temporarily disabled -->
    {:else if geometry.type === 'bibi'}
      <Bibanime 
        position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
        scale={5} 
      />
    {:else if geometry.type === 'tissus'}
      <Tissus 
        position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
        scale={5} 
      />
    {:else if geometry.type === 'vague'}
      {console.log('Vague position:', [geometry.position.x, geometry.position.y, geometry.position.z])}
      <Vague 
        position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
        rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
        scale={5}
      />
    {:else if geometry.type === 'desk'}
      {console.log('Desk position:', [geometry.position.x, geometry.position.y, geometry.position.z])}
      <Desk 
        position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
        rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
        scale={5}
      />
    {:else if geometry.type === 'sphere'}
      <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
        rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
        <T.SphereGeometry />
        <T.MeshStandardMaterial color={geometry.color} />
      </T.Mesh>
    {:else if geometry.type === 'bibigame'}
      <Bibigame />
    {/if}
  </Float>
{/each}

 


