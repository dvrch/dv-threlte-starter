<script lang="ts">
	import { T, useLoader } from '@threlte/core';
	import { TextureLoader } from 'three';
	import * as THREE from 'three';
	import { Group } from 'three';
	import GltfModel from '$lib/components/GltfModel.svelte';
	import { browser } from '$app/environment';
	import { Text3DGeometry } from '@threlte/extras';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';

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
		textmd: () => import('$lib/components/TextMd.svelte')
	};

	const DynamicComponentLoader = $derived(() => {
		const name = (geometry?.name || '').toLowerCase();
		const url = (geometry?.model_url || '').toLowerCase();
		const type = (geometry?.type || '').toLowerCase();

		if (
			type === 'spaceship' ||
			name.includes('spaceship') ||
			url.includes('spaceship.glb') ||
			(name.includes('ship') && type !== 'bibi')
		) {
			return componentMap['spaceship'];
		}

		if (type === 'nissangame' || type === 'nissan' || name.includes('nissangame')) {
			return componentMap['nissangame'];
		}

		if (name.toLowerCase().includes('textmd') || name.toLowerCase().includes('cv')) {
			return componentMap['textmd'];
		}

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

	const imageUrl = $derived(() => {
		const rawUrl = geometry?.model_url;
		if (!rawUrl) return null;

		const isImage =
			geometry.type === 'image_plane' || /\.(jpg|jpeg|png|webp|gif|svg)$/i.test(rawUrl);

		if (!isImage) return null;

		const cleaned = getCloudinaryAssetUrl(rawUrl);
		return cleaned;
	});

	const loader = useLoader(TextureLoader);
	const textureStore = $derived(imageUrl() ? loader.load(imageUrl()!) : null);

	let aspect = $state(1);
	$effect(() => {
		if (textureStore && $textureStore) {
			const tex = $textureStore as THREE.Texture;

			const checkImage = () => {
				if (tex.image && tex.image.width > 0) {
					aspect = tex.image.width / tex.image.height;
					console.log(`✅ [ImagePlane] Aspect Ready: ${aspect} for ${geometry.name}`);
				}
			};

			checkImage();

			if (!tex.image || tex.image.width === 0) {
				tex.addEventListener('update', checkImage);
				if (tex.source && tex.source.data instanceof HTMLImageElement) {
					tex.source.data.onload = checkImage;
				}
			}

			return () => {
				tex.removeEventListener('update', checkImage);
			};
		}
	});

	$effect(() => {
		const url = imageUrl();
		if (url) {
			console.log('🖼️ [ImagePlane] Target URL:', url);
		}
	});
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
		{:else if imageUrl()}
			<!-- Face camera logic: PlaneGeometry faces +Z. We scale by aspect ratio. -->
			<T.Mesh
				name="ImagePlaneMesh"
				scale={[aspect, 1, 1]}
				position={[0, 0, 0.02]}
				frustumCulled={false}
			>
				<T.PlaneGeometry args={[5, 5]} />
				{#if textureStore && $textureStore}
					<T.MeshBasicMaterial
						map={$textureStore as any}
						color="white"
						side={THREE.DoubleSide}
						transparent={true}
						toneMapped={false}
						depthWrite={true}
						opacity={1}
					/>
				{:else}
					<!-- Fallback loader -->
					<T.MeshBasicMaterial
						color="#333333"
						side={THREE.DoubleSide}
						opacity={0.5}
						transparent={true}
					/>
				{/if}
			</T.Mesh>
		{:else if geometry.model_url && geometry.model_url.trim() !== ''}
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
