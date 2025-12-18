<script lang="ts">
	import { T } from '@threlte/core';
	import GltfModel from '$lib/components/GltfModel.svelte';
	import { browser } from '$app/environment';
	import { Text3DGeometry } from '@threlte/extras';

	// 🌐 Font pour le texte 3D
	const font =
		'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/fonts/helvetiker_bold.typeface.json';

	let { geometry }: { geometry: any } = $props();

	// Map geometry types to their respective Svelte components using dynamic imports
	const componentMap: { [key: string]: () => Promise<any> } = {
		vague: () => import('../../routes/vague/vague.svelte'),
		tissus: () => import('../../routes/bibi/tissus-simulat.svelte'),
		desk: () => import('../../routes/desksc/scene.svelte'), // Corrected case
		nissan: () => import('../../routes/app/models/Nissan.svelte'),
		bibi: () => import('../../routes/bibi/bibanime.svelte'),
		garden: () => import('../../routes/app/models/garden.svelte'),
		nissangame: () => import('../../routes/app/nissangame.svelte'),
		bibigame: () => import('../../routes/app/bibigame.svelte')
	};

	const DynamicComponentLoader = $derived(componentMap[geometry?.type] ?? null);
	let LoadedDynamicComponent: any = $state(null); // To store the dynamically loaded component

	// Load the component dynamically only on the client
	$effect(() => {
		if (browser && DynamicComponentLoader) {
			LoadedDynamicComponent = null; // Reset before loading new component
			DynamicComponentLoader()
				.then((module) => {
					LoadedDynamicComponent = module.default;
				})
				.catch((error) => {
					console.error(`Failed to load dynamic component for type '${geometry.type}':`, error);
					LoadedDynamicComponent = null;
				});
		} else {
			LoadedDynamicComponent = null;
		}
	});

	// reactive safe position/rotation/scale arrays
	const posArray: [number, number, number] = $derived([
		geometry?.position?.x ?? 0,
		geometry?.position?.y ?? 0,
		geometry?.position?.z ?? 0
	]);
	const rotArray: [number, number, number] = $derived([
		geometry?.rotation?.x ?? 0,
		geometry?.rotation?.y ?? 0,
		geometry?.rotation?.z ?? 0
	]);
	const scaleArray: [number, number, number] = $derived([
		geometry?.scale?.x ?? 1,
		geometry?.scale?.y ?? 1,
		geometry?.scale?.z ?? 1
	]);
</script>

{#if browser && geometry}
	<T.Group position={posArray} rotation={rotArray} scale={scaleArray}>
		{#if LoadedDynamicComponent}
			<!-- 1. Render the dynamically loaded Svelte component when available -->
			{@const Component = LoadedDynamicComponent}
			<Component {geometry} />
		{:else if geometry.type === 'text'}
			<T.Mesh>
				<Text3DGeometry {font} text={geometry.name} size={1} height={1} curveSegments={12} />
				<T.MeshStandardMaterial color={geometry.color} />
			</T.Mesh>
		{:else if geometry.model_url && geometry.model_url.trim() !== ''}
			<!-- 2. Render a generic GLTF model if model_url is present and valid -->
			{@const modelUrl = geometry.model_url}
			{#key modelUrl}
				<GltfModel url={modelUrl} />
			{/key}
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
