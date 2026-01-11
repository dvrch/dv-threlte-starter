<script lang="ts">
	import { T } from '@threlte/core';
	import * as THREE from 'three';
	import { Group } from 'three';
	import GltfModel from '$lib/components/GltfModel.svelte';
	import { browser } from '$app/environment';
	import { Text3DGeometry, HTML } from '@threlte/extras';

	// 🌐 Font pour le texte 3D
	const font =
		'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/fonts/helvetiker_bold.typeface.json';

	interface GeometryData {
		id: string | number;
		name: string;
		type: string;
		model_url?: string;
		model_type?: string;
		position: { x: number; y: number; z: number };
		rotation: { x: number; y: number; z: number };
		scale: { x: number; y: number; z: number };
		color: string;
		visible: boolean;
		markdown_content?: string;
	}

	let {
		geometry,
		ref = $bindable(new Group()),
		onPointerDown
	}: { geometry: GeometryData; ref?: Group; onPointerDown?: () => void } = $props();

	$effect(() => {
		console.log(
			'📦 [Dynamic3DModel] Rendering:',
			geometry.name,
			'| Type:',
			geometry.type,
			'| URL:',
			geometry.model_url,
			'| Has MD:',
			!!geometry.markdown_content
		);
	});

	// Map geometry types to their respective Svelte components using dynamic imports
	const componentMap: { [key: string]: () => Promise<any> } = {
		vague: () => import('../../routes/vague/vaguend.svelte'),
		tissus: () => import('$lib/components/Cloth.svelte'),
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

		// Priority 1: Image Plane / Cloth
		if (type === 'image_plane') return componentMap['image_plane'];
		if (type === 'tissus' || type === 'cloth') return componentMap['tissus'];

		// Auto-detection by URL
		if (url && /\.(jpg|jpeg|png|webp|gif|svg)$/i.test(url)) {
			return componentMap['image_plane'];
		}

		// Priority 2: MD
		if (type === 'textmd' || name.toLowerCase().includes('textmd')) {
			return componentMap['textmd'];
		}

		// Priority 3: Spaceship
		if (type === 'spaceship' || name.includes('spaceship') || url.includes('spaceship.glb')) {
			return componentMap['spaceship'];
		}

		// Priority 4: Nissan
		if (type === 'nissangame' || type === 'nissan') {
			return componentMap['nissangame'];
		}

		// Priority 5: Standard
		return componentMap[type] ?? null;
	});

	let LoadedDynamicComponent: any = $state(null);

	$effect(() => {
		const loader = DynamicComponentLoader();
		if (browser && loader) {
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
</script>

<T.Group
	bind:ref
	position={[geometry.position.x, geometry.position.y, geometry.position.z]}
	rotation={[
		THREE.MathUtils.degToRad(geometry.rotation.x),
		THREE.MathUtils.degToRad(geometry.rotation.y),
		THREE.MathUtils.degToRad(geometry.rotation.z)
	]}
	scale={[geometry.scale.x, geometry.scale.y, geometry.scale.z]}
	visible={geometry.visible}
	onpointerdown={(e: any) => {
		e.stopPropagation();
		onPointerDown?.();
	}}
>
	{#if geometry.type === 'gltf_model' && geometry.model_url}
		<GltfModel url={geometry.model_url} {geometry} />
	{:else if LoadedDynamicComponent}
		{@const Component = LoadedDynamicComponent}
		{#if geometry.type === 'text_scene'}
			<Component
				{geometry}
				cvLines={geometry.markdown_content
					? geometry.markdown_content.split('\n').filter((l) => l.trim())
					: []}
			/>
		{:else}
			<Component
				{geometry}
				cvLines={geometry.markdown_content
					? geometry.markdown_content.split('\n').filter((l) => l.trim())
					: []}
			/>
		{/if}
	{:else if geometry.type === 'text'}
		<T.Mesh scale={[geometry.scale?.x ?? 1, 1, 0.001]}>
			<Text3DGeometry {font} text={geometry.name} size={0.5} height={0.5} />
			<T.MeshStandardMaterial color={geometry.color} metalness={0.8} roughness={0.2} />
		</T.Mesh>
	{:else if geometry.type === 'box'}
		<T.Mesh>
			<T.BoxGeometry args={[1, 1, 1]} />
			<T.MeshStandardMaterial color={geometry.color} metalness={0.5} roughness={0.5} />
		</T.Mesh>
	{:else if geometry.type === 'sphere'}
		<T.Mesh>
			<T.SphereGeometry args={[0.5, 32, 32]} />
			<T.MeshStandardMaterial color={geometry.color} metalness={0.5} roughness={0.5} />
		</T.Mesh>
	{:else if geometry.type === 'plane'}
		<T.Mesh rotation.x={THREE.MathUtils.degToRad(-90)}>
			<T.PlaneGeometry args={[1, 1]} />
			<T.MeshStandardMaterial
				color={geometry.color}
				side={THREE.DoubleSide}
				metalness={0.5}
				roughness={0.5}
			/>
		</T.Mesh>
	{:else}
		<T.Mesh>
			<T.BoxGeometry args={[0.2, 0.2, 0.2]} />
			<T.MeshBasicMaterial color="red" wireframe />
			<HTML>
				<div style="color: white; background: rgba(0,0,0,0.5); padding: 2px;">
					{geometry.type}
				</div>
			</HTML>
		</T.Mesh>
	{/if}
</T.Group>
