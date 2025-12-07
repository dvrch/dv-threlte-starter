<script lang="ts">
	import { T } from '@threlte/core';
	import GltfModel from '$lib/components/GltfModel.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte'; // Need onMount for dynamic imports

	import { getAssetUrl } from '$lib/asset-helper';

	let { geometry }: { geometry: any } = $props();

	// Map geometry types to their respective Svelte components using dynamic imports
	const componentMap: { [key: string]: () => Promise<any> } = {
		sphere: () => import('../../routes/sphere/+page.svelte'),
		vague: () => import('../../routes/vague/+page.svelte'),
		tissus: () => import('../../routes/bibi/tissus-simulat.svelte'),
		desk: () => import('../../routes/desksc/+page.svelte'),
		// nissan: () => import('../../routes/Spaceship/Nissan.svelte'), // Temporarily disabled
		bibi: () => import('../../routes/bibi/bibanime.svelte'),
		// garden: () => import('../../routes/app/models/garden.svelte'), // Temporarily disabled
		nissangame: () => import('../../routes/app/nissangame.svelte'),
		bibigame: () => import('../../routes/app/bibigame.svelte')
	};

	const DynamicComponentLoader = $derived(componentMap[geometry?.type] ?? null);
	let LoadedDynamicComponent: any = $state(null); // To store the dynamically loaded component

	// Load the component dynamically only on the client
	$effect(() => {
		if (browser && DynamicComponentLoader) {
			LoadedDynamicComponent = null; // Reset before loading new component
			DynamicComponentLoader().then(module => {
				LoadedDynamicComponent = module.default;
			}).catch(error => {
				console.error(`Failed to load dynamic component for type '${geometry.type}':`, error);
				LoadedDynamicComponent = null;
			});
		} else {
			LoadedDynamicComponent = null;
		}
	});

	// reactive safe position/rotation arrays
	const posArray = $derived([geometry?.position?.x ?? 0, geometry?.position?.y ?? 0, geometry?.position?.z ?? 0]);
	const rotArray = $derived([geometry?.rotation?.x ?? 0, geometry?.rotation?.y ?? 0, geometry?.rotation?.z ?? 0]);
</script>

{#if browser && geometry}
	<T.Group position={posArray} rotation={rotArray} scale={geometry.scale ?? 1}>
		{#if LoadedDynamicComponent}
			<!-- 1. Render the dynamically loaded Svelte component when available -->
			{@const Component = LoadedDynamicComponent}
			<Component {geometry} />
		{:else if geometry.model_url}
			<!-- 2. Render a generic GLTF model if model_url is present -->
			<GltfModel url={getAssetUrl(geometry.model_url)} />
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
{/if}
