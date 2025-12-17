<script lang="ts">
	import Bibigame from './bibigame.svelte';
	import { onMount, onDestroy } from 'svelte';
	import { writable } from 'svelte/store';
	import Nissangame from './nissangame.svelte';
	import { T } from '@threlte/core';
	import { ContactShadows, Float, Grid, OrbitControls, Text } from '@threlte/extras';
	import Bloom from './models/bloom.svelte';
	import AddGeometry from './AddGeometry.svelte';
	import { addToast } from '$lib/stores/toasts';
	import GltfModel from '$lib/components/GltfModel.svelte';

	// Import simplifiés - les originaux sont désactivés car ils utilisent des Canvas complexes
	// import Tissus from '../bibi/tissus-simulat.svelte';
	// import Bibanime from '../bibi/bibanime.svelte';
	// import Vague from '../vague/+page.svelte';
	// import Spaceship from '../Spaceship/+page.svelte';
	// import Desk from '../desksc/+page.svelte';

	import { assets } from '$lib/services/assets';
	import { GeometriesRepository, type Geometry } from '$lib/repositories/geometries';

	let geometries: any[] = $state([]);

	const selectedGeometry: any = writable(null);

	const handleGeometryClick = (geometry: Geometry) => {
		$selectedGeometry = geometry;
	};

	const deleteGeometry = async (id: string) => {
		try {
			await GeometriesRepository.delete(id);
			loadGeometries();
			addToast('Geometry deleted successfully!', 'success');
		} catch (error) {
			console.error('Error deleting geometry:', error);
			addToast('Failed to delete geometry. Please try again.', 'error');
		}
	};

	const loadGeometries = async () => {
		try {
			const data = await GeometriesRepository.getAll();
			console.log('Loaded geometries:', data);

			// Gestion de la pagination Django Rest Framework (results) ou liste directe
			if (data && 'results' in data && Array.isArray(data.results)) {
				geometries = data.results;
			} else if (Array.isArray(data)) {
				geometries = data;
			} else {
				console.error('Unexpected data format for geometries:', data);
				geometries = [];
			}
		} catch (error) {
			console.error('Error loading geometries:', error);
			// addToast('Error loading geometries', 'error'); // Optionnel
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
		selectedGeometry.set(null);
	};
</script>

<T.PerspectiveCamera makeDefault position={[15, 15, 15]} fov={50}>
	<OrbitControls enableDamping enableZoom enableRotate enablePan />
</T.PerspectiveCamera>

<T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
<T.AmbientLight intensity={0.2} />

<Grid
	position={[0, -0.001, 0]}
	cellColor="#ffffff"
	sectionColor="#ffffff"
	sectionThickness={0}
	fadeDistance={25}
	cellSize={2}
/>

<ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />

<Bloom />

<AddGeometry selectedGeometry={$selectedGeometry} on:geometryChanged={handleGeometryChange} />

{#each geometries as geometry (geometry.id)}
	<Float floatIntensity={1} floatingRange={[0, 1]} on:click={() => handleGeometryClick(geometry)}>
		{#if geometry.model_url}
			<GltfModel
				url={assets.getUrl(geometry.model_url)}
				position={geometry.position}
				rotation={geometry.rotation}
			/>
		{:else if geometry.type === 'box'}
			<T.Mesh
				position={[geometry.position.x, geometry.position.y, geometry.position.z]}
				rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
				scale={0.5}
			>
				<T.BoxGeometry args={[2, 2, 2]} />
				<T.MeshStandardMaterial color={geometry.color} />
			</T.Mesh>
		{:else if geometry.type === 'torus'}
			<T.Mesh
				position={[geometry.position.x, geometry.position.y, geometry.position.z]}
				rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
				scale={0.5}
			>
				<T.TorusKnotGeometry args={[0.5, 0.15, 100, 12, 2, 3]} />
				<T.MeshStandardMaterial color={geometry.color} />
			</T.Mesh>
		{:else if geometry.type === 'icosahedron'}
			<T.Mesh
				position={[geometry.position.x, geometry.position.y, geometry.position.z]}
				rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
				scale={0.5}
			>
				<T.IcosahedronGeometry args={[1, 0]} />
				<T.MeshStandardMaterial color={geometry.color} />
			</T.Mesh>
		{:else if geometry.type === 'nissangame'}
			<Nissangame {geometry} />
		{:else if geometry.type === 'garden'}
			<!-- Garden temporarily disabled -->
		{:else if geometry.type === 'nissan'}
			<!-- Nissan temporarily disabled -->
		{:else if geometry.type === 'bibi'}
			<!-- Bibanime temporarily disabled - needs Canvas wrapper -->
		{:else if geometry.type === 'tissus'}
			<!-- Tissus simplified - plane with textile texture -->
			<T.Group position={[geometry.position.x, geometry.position.y, geometry.position.z]}>
				<T.Mesh position={[0, 0, 0]}>
					<T.PlaneGeometry args={[6, 6]} />
					<T.MeshStandardMaterial color="#87CEEB" opacity={0.8} />
				</T.Mesh>
			</T.Group>
		{:else if geometry.type === 'vague'}
			<!-- Vague simplified - animated wave plane -->
			<T.Group position={[geometry.position.x, geometry.position.y, geometry.position.z]}>
				<T.Mesh position={[0, 0, 0]}>
					<T.PlaneGeometry args={[5, 5]} />
					<T.MeshStandardMaterial color="#4169E1" opacity={0.8} />
				</T.Mesh>
				<!-- Animated waves effect -->
				<T.Mesh position={[0, 0.1, 0]}>
					<T.PlaneGeometry args={[4.8, 4.8]} />
					<T.MeshStandardMaterial color="#2980b9" opacity={0.6} />
				</T.Mesh>
			</T.Group>
		{:else if geometry.type === 'desk'}
			{console.log('Desk position:', [
				geometry.position.x,
				geometry.position.y,
				geometry.position.z
			])}
			<!-- Desk simplified - box with brown color -->
			<T.Group position={[geometry.position.x, geometry.position.y, geometry.position.z]} scale={5}>
				<T.BoxGeometry args={[4, 2, 3]} />
				<T.MeshStandardMaterial color="#8B4513" />
			</T.Group>
		{:else if geometry.type === 'sphere'}
			<T.Mesh
				position={[geometry.position.x, geometry.position.y, geometry.position.z]}
				rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
				scale={0.5}
			>
				<T.SphereGeometry />
				<T.MeshStandardMaterial color={geometry.color} />
			</T.Mesh>
		{:else if geometry.type === 'bibigame'}
			<Bibigame />
		{:else if geometry.type === 'text'}
			<Text
				text={geometry.name}
				position={[geometry.position.x, geometry.position.y, geometry.position.z]}
				rotation={[
					geometry.rotation.x * (Math.PI / 180),
					geometry.rotation.y * (Math.PI / 180),
					geometry.rotation.z * (Math.PI / 180)
				]}
				scale={[geometry.scale?.x || 1, geometry.scale?.y || 1, geometry.scale?.z || 1]}
				color={geometry.color}
				fontSize={1}
				anchorX="center"
				anchorY="middle"
			/>
		{/if}
	</Float>
{/each}
