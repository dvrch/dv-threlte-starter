<script lang="ts">
	import { T } from '@threlte/core';
	import * as THREE from 'three';
	import { Group } from 'three';
	import GltfModel from '$lib/components/GltfModel.svelte';
	import { browser } from '$app/environment';
	import { Text3DGeometry } from '@threlte/extras';

	// 🌐 Font pour le texte 3D
	const font =
		'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/fonts/helvetiker_bold.typeface.json';

	interface GeometryData {
		id: number;
		name: string;
		type: string;
		model_url?: string;
		model_type?: string;
		position: { x: number; y: number; z: number };
		rotation: { x: number; y: number; z: number };
		scale: { x: number; y: number; z: number };
		color: string;
		visible: boolean;
	}

	let {
		geometry,
		ref = $bindable(new Group()),
		onPointerDown
	}: { geometry: GeometryData; ref?: Group; onPointerDown?: () => void } = $props();

	// Map geometry types to their respective Svelte components using dynamic imports
	const componentMap: { [key: string]: () => Promise<any> } = {
		vague: () => import('../../routes/vague/vaguend.svelte'),
		tissus: () => import('../../routes/bibi/tissus-simulat.svelte'),
		desk: () => import('../../routes/desksc/scene.svelte'),
		nissan: () => import('../../routes/app/models/Nissan.svelte'),
		bibi: () => import('../../routes/bibi/bibanime.svelte'),
		garden: () => import('../../routes/app/models/garden.svelte'),
		nissangame: () => import('../../routes/app/nissangame.svelte'),
		bibigame: () => import('../../routes/app/bibigame.svelte'),
		spaceship: () => import('../../routes/app/models/spaceship.svelte'),
		text_scene: () => import('../../routes/Text/scene.svelte'),
		textmd: () => import('$lib/components/TextMd.svelte'),
		image_plane: () => import('$lib/components/ImagePlane.svelte')
	};

	const DynamicComponentLoader = $derived(() => {
		const name = (geometry?.name || '').toLowerCase();
		const url = (geometry?.model_url || '').toLowerCase();
		const type = (geometry?.type || '').toLowerCase();

		// Priority 1: Image Plane (Direct match)
		if (type === 'image_plane' || (url && /\.(jpg|jpeg|png|webp|gif|svg)$/i.test(url))) {
			return componentMap['image_plane'];
		}

		// Priority 2: Special detection by URL or Name for Spaceship
		if (
			type === 'spaceship' ||
			name.includes('spaceship') ||
			url.includes('spaceship.glb') ||
			(name.includes('ship') && type !== 'bibi')
		) {
			return componentMap['spaceship'];
		}

		// Priority 3: Detection for Nissan Game
		if (type === 'nissangame' || type === 'nissan' || name.includes('nissangame')) {
			return componentMap['nissangame'];
		}

		// Priority 4: Detection for textmd
		if (name.toLowerCase().includes('textmd') || name.toLowerCase().includes('cv')) {
			return componentMap['textmd'];
		}

		// Priority 5: Standard type mapping
		return componentMap[type] ?? null;
	});

	let LoadedDynamicComponent: any = $state(null);

	$effect(() => {
		const loader = DynamicComponentLoader();
		if (browser && loader) {
			LoadedDynamicComponent = null;
			loader()
				.then((module) => {
					LoadedDynamicComponent = module.default;
				})
				.catch((error) => {
					console.error(`Failed to load dynamic component for ${geometry.type}:`, error);
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
	const DEG2RAD = Math.PI / 180;
	const rotArray: [number, number, number] = $derived([
		(geometry?.rotation?.x ?? 0) * DEG2RAD,
		(geometry?.rotation?.y ?? 0) * DEG2RAD,
		(geometry?.rotation?.z ?? 0) * DEG2RAD
	]);
	const scaleArray: [number, number, number] = $derived([
		geometry?.scale?.x ?? 1,
		geometry?.scale?.y ?? 1,
		geometry?.scale?.z ?? 1
	]);
</script>

{#if browser && geometry}
	<T.Group
		is={ref}
		position={posArray}
		rotation={rotArray}
		scale={scaleArray}
		visible={geometry.visible !== false}
		onpointerdown={(e: any) => {
			if (onPointerDown) {
				e.stopPropagation();
				onPointerDown();
			}
		}}
	>
		{#if LoadedDynamicComponent}
			{@const Component = LoadedDynamicComponent}
			{#if geometry.type === 'text_scene'}
				<Component
					cvLines={[
						'# Welcome',
						'## To the 3D Editor',
						'Interactive Elements',
						'- Drag & Drop GLB',
						'- Real-time Sync',
						'- Physics Games'
					]}
					{geometry}
				/>
			{:else}
				<Component {geometry} />
			{/if}
		{:else if geometry.type === 'text'}
			<T.Mesh scale={[geometry.scale?.x ?? 1, 1, 0.001]}>
				<Text3DGeometry
					{font}
					text={geometry.name}
					size={geometry.scale?.y ?? 1}
					height={geometry.scale?.z ?? 0.01}
					curveSegments={12}
				/>
				<T.MeshStandardMaterial color={geometry.color} />
			</T.Mesh>
		{:else if geometry.model_url && geometry.model_url.trim() !== '' && !/\.(jpg|jpeg|png|webp|gif|svg)$/i.test(geometry.model_url) && geometry.type !== 'image_plane'}
			<GltfModel url={geometry.model_url} />
		{:else if geometry.type === 'box'}
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
			<T.Mesh>
				<T.BoxGeometry />
				<T.MeshStandardMaterial color="purple" />
			</T.Mesh>
		{/if}
	</T.Group>
{/if}
