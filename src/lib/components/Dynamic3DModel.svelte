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
	
	$: {
	if (geometry && geometry.model_type === 'from_file' && geometry.type) {
	DynamicComponent = componentMap[geometry.type];
	if (!DynamicComponent) {
	console.error(`No component found for type: ${geometry.type}`);
	}
	} else {
	DynamicComponent = null;
	}
	}
	</script>
	
	<!-- 
	  New rendering logic with strict precedence:
	  1. GLTF models via `model_url`.
	  2. Dynamic Svelte components via `model_type === 'from_file'`.
	  3. Basic primitive shapes via `type`.
	-->
	
	<T.Group
	position={[geometry.position.x, geometry.position.y, geometry.position.z]}
	rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
	scale={geometry.scale || 1}
	>
	{#if geometry.model_url}
		<!-- 1. Render a GLTF model if model_url is present -->
		<GltfModel url={geometry.model_url} />
	{:else if geometry.model_type === 'from_file'}
		<!-- 2. Render the dynamically loaded Svelte component -->
		{#if DynamicComponent}
			<svelte:component this={DynamicComponent} />
		{:else}
			<!-- Error fallback: component was expected but not found in map -->
			<T.Mesh>
				<T.BoxGeometry />
				<T.MeshStandardMaterial color="red" />
			</T.Mesh>
		{/if}
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
	<!-- Defensive access to avoid runtime errors when geometry fields are missing -->
	{#if geometry}
		{#let pos = geometry.position ?? { x: 0, y: 0, z: 0 }}
		{#let rot = geometry.rotation ?? { x: 0, y: 0, z: 0 }}
		<T.Group
			position={[pos.x ?? 0, pos.y ?? 0, pos.z ?? 0]}
			rotation={[rot.x ?? 0, rot.y ?? 0, rot.z ?? 0]}
			scale={geometry.scale ?? 1}
		>
