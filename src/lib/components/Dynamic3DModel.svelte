<script lang="ts">
	// Use the named `T` import consistently with other components
	import { T } from '@threlte/core';
	import GltfModel from '$lib/components/GltfModel.svelte';
	
	// Import all known Svelte components
	import SpherePage from '../../routes/sphere/+page.svelte';
	import VaguePage from '../../routes/vague/+page.svelte';
	import TissusSimulat from '../../routes/bibi/tissus-simulat.svelte';
	import DeskPage from '../../routes/desksc/+page.svelte';
	import NissanComponent from '../../routes/Spaceship/Nissan.svelte';
	import Bibianime from '../../routes/bibi/bibanime.svelte';
	import GardenComponent from '../../routes/app/models/garden.svelte';
	import NissangameComponent from '../../routes/app/nissangame.svelte';
	import BibigameComponent from '../../routes/app/bibigame.svelte';
	
	export let geometry: any;
	
	// Map geometry types to their respective Svelte components
	const componentMap: { [key: string]: any } = {
	sphere: SpherePage,
	vague: VaguePage,
	tissus: TissusSimulat,
	desk: DeskPage,
	nissan: NissanComponent,
	bibi: Bibianime,
	garden: GardenComponent,
	nissangame: NissangameComponent,
	bibigame: BibigameComponent
	};
	
	let DynamicComponent: any = null;
	
	// Determine dynamic component from geometry.type when available.
	// Some geometries in the DB may not set `model_type`, so prefer matching by `type`.
	$: {
		if (geometry && geometry.type) {
			DynamicComponent = componentMap[geometry.type];
			if (!DynamicComponent) {
				// not fatal, we fallback to primitives below — helpful debug log
				console.debug(`Dynamic3DModel: no mapped component for type='${geometry.type}'`);
			}
		} else {
			DynamicComponent = null;
		}
	}

	// reactive safe position/rotation arrays
	$: posArray = [geometry?.position?.x ?? 0, geometry?.position?.y ?? 0, geometry?.position?.z ?? 0];
	$: rotArray = [geometry?.rotation?.x ?? 0, geometry?.rotation?.y ?? 0, geometry?.rotation?.z ?? 0];
	</script>
	
	<!-- 
		New rendering logic with strict precedence:
		1. Dynamic Svelte components via `type` mapping.
		2. GLTF models via `model_url` (for types without a specific component).
		3. Basic primitive shapes via `type`.
	-->

	<!-- compute safe position/rotation arrays to avoid runtime exceptions -->

	{#if geometry}

		<T.Group position={posArray} rotation={rotArray} scale={geometry.scale ?? 1}>
			{#if DynamicComponent}
				<!-- 1. Render the dynamically loaded Svelte component when available -->
				<svelte:component this={DynamicComponent} {...geometry} url={geometry.model_url} />
			{:else if geometry.model_url}
				<!-- 2. Render a generic GLTF model if model_url is present -->
				<GltfModel url={geometry.model_url} />
			{:else if geometry.type === 'box'}
				<!-- 3. Render primitive shapes -->
				<T.Mesh>
					<T.BoxGeometry />
					<T.MeshStandardMaterial color={geometry.color} />
				</T.Mesh>
			{:else if geometry.type === 'torus'}
				<T.Mesh>
					<T.TorusKnotGeometry args={[0.5, 0.15, 100, 12, 2, 3]} />
					<T.MeshStandardMaterial color={geometry.color} />
				</T.Mesh>
			{:else if geometry.type === 'icosahedron'}
				<T.Mesh>
					<T.IcosahedronGeometry />
					<T.MeshStandardMaterial color={geometry.color} />
				</T.Mesh>
			{:else if geometry.type === 'sphere'}
				<T.Mesh>
					<T.SphereGeometry />
					<T.MeshStandardMaterial color={geometry.color} />
				</T.Mesh>
			{:else}
				<!-- Fallback for completely unhandled types -->
				<T.Mesh>
					<T.BoxGeometry />
					<T.MeshStandardMaterial color="purple" />
				</T.Mesh>
			{/if}
		</T.Group>
	{:else}
		<!-- If geometry missing, render nothing (or a tiny marker) -->
		<T.Group />
	{/if}
