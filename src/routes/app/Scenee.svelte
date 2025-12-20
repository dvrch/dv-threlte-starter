<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { writable } from 'svelte/store';
	import { T, useThrelte } from '@threlte/core';
	import { ContactShadows, Float, Grid, OrbitControls } from '@threlte/extras';
	import Bloom from './models/bloom.svelte';
	import AddGeometry from './AddGeometry.svelte';
	import { addToast } from '$lib/stores/toasts';
	import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
	import { GeometriesRepository, type Geometry } from '$lib/repositories/geometries';

	let geometries: any[] = $state([]);
	const selectedGeometry: any = writable(null);

	const handleGeometryClick = (geometry: Geometry) => {
		selectedGeometry.set(geometry);
	};

	const loadGeometries = async () => {
		try {
			const data = await GeometriesRepository.getAll();
			if (data && 'results' in data && Array.isArray(data.results)) {
				geometries = data.results;
			} else if (Array.isArray(data)) {
				geometries = data;
			} else {
				geometries = [];
			}
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
	{#if geometry.visible}
		<Float floatIntensity={1} floatingRange={[0, 1]} on:click={() => handleGeometryClick(geometry)}>
			<Dynamic3DModel {geometry} />
		</Float>
	{/if}
{/each}
