<script lang="ts">
	import { T, Canvas } from '@threlte/core';
	import {
		Float,
		Grid,
		HTML,
		OrbitControls,
		Environment,
		TransformControls,
		Outlines
	} from '@threlte/extras';
	import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { Group } from 'three';
	import { HDRLoader } from 'three/examples/jsm/loaders/HDRLoader.js'; // Future-proof if we go manual

	import { addToast } from '$lib/stores/toasts';
	import Bloom from './models/bloom.svelte';
	import Stars from '../Spaceship/Stars.svelte';
	import ScenePremiumEffects from './components/ScenePremiumEffects.svelte';
	import SceneText2 from '../Text/scene.svelte';

	import { geometryService, type GeometryItem } from '$lib/services/api';

	let geometries = $state<GeometryItem[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let isBloomEnabled = $state(true); // State to control Bloom effect
	let isPremiumEnabled = $state(true); // Premium Effects Toggle

	// Transform Controls State
	let transformSettings = $state({
		enabled: false,
		selectedId: '',
		modes: ['translate', 'rotate', 'scale'] as ('translate' | 'rotate' | 'scale')[]
	});

	// Store for model refs
	let modelRefs = $state<Record<string, Group>>({});

	// Function to fetch geometries
	const fetchGeometries = async () => {
		try {
			loading = true;
			const results = await geometryService.getAll();

			geometries = results.filter((g: any) => {
				if (g.type === 'gltf' || g.type === 'glb' || g.type === 'gltf_model') {
					return true;
				}
				return true;
			});

			// Pre-initialize model refs
			geometries.forEach((g) => {
				if (!modelRefs[g.id]) {
					modelRefs[g.id] = new Group();
				}
			});

			console.log('✅ Loaded geometries:', geometries.length);
		} catch (e) {
			error = (e as Error).message;
			console.error('❌ Error loading geometries:', e);
		} finally {
			loading = false;
		}
	};

	const syncGeometry = (geometry: GeometryItem, obj: Group) => {
		if (obj && geometry) {
			geometry.position = {
				x: Number(obj.position.x.toFixed(2)),
				y: Number(obj.position.y.toFixed(2)),
				z: Number(obj.position.z.toFixed(2))
			};
			geometry.rotation = {
				x: Number((obj.rotation.x * (180 / Math.PI)).toFixed(2)),
				y: Number((obj.rotation.y * (180 / Math.PI)).toFixed(2)),
				z: Number((obj.rotation.z * (180 / Math.PI)).toFixed(2))
			};
			geometry.scale = {
				x: Number(obj.scale.x.toFixed(2)),
				y: Number(obj.scale.y.toFixed(2)),
				z: Number(obj.scale.z.toFixed(2))
			};

			window.dispatchEvent(
				new CustomEvent('manualTransformSync', {
					detail: {
						id: geometry.id,
						position: geometry.position,
						rotation: geometry.rotation,
						scale: geometry.scale
					}
				})
			);
		}
	};

	onMount(() => {
		fetchGeometries();
		window.addEventListener('modelAdded', fetchGeometries);

		const handleVisibilityChange = (event: Event) => {
			const customEvent = event as CustomEvent;
			const { id, visible } = customEvent.detail;
			if (typeof visible !== 'boolean') return;
			geometries = geometries.map((g) => (g.id == id ? { ...g, visible: visible } : g));
		};
		window.addEventListener('geometryVisibilityChanged', handleVisibilityChange);

		const handleToggleBloom = (event: Event) => {
			const customEvent = event as CustomEvent;
			isBloomEnabled = customEvent.detail.enabled;
		};
		window.addEventListener('toggleBloomEffect', handleToggleBloom);

		const handleTogglePremium = (event: Event) => {
			const customEvent = event as CustomEvent;
			isPremiumEnabled = customEvent.detail.enabled;
		};
		window.addEventListener('togglePremiumEffect', handleTogglePremium);

		const handleToggleTransform = (event: Event) => {
			const customEvent = event as CustomEvent;
			transformSettings = {
				enabled: customEvent.detail.enabled,
				selectedId: customEvent.detail.id,
				modes: customEvent.detail.modes || ['translate']
			};
		};
		window.addEventListener('toggleTransformControls', handleToggleTransform);

		return () => {
			window.removeEventListener('modelAdded', fetchGeometries);
			window.removeEventListener('geometryVisibilityChanged', handleVisibilityChange);
			window.removeEventListener('toggleBloomEffect', handleToggleBloom);
			window.removeEventListener('togglePremiumEffect', handleTogglePremium);
			window.removeEventListener('toggleTransformControls', handleToggleTransform);
		};
	});
</script>

<T.AmbientLight intensity={isPremiumEnabled ? 1.0 : 1.5} />
<T.DirectionalLight position={[10, 10, 10]} intensity={5} castShadow />
<T.DirectionalLight position={[-10, 5, -10]} intensity={3} color="#4287f5" />
<T.HemisphereLight intensity={1.0} groundColor="#444444" skyColor="#ffffff" />

<Stars />

<HTML center>
	{#if error}
		<div class="error">Erreur: {error}</div>
	{:else if loading}
		<div class="loading">Chargement des géométries...</div>
	{:else if geometries.length === 0}
		<div class="empty">Aucune géométrie trouvée</div>
	{/if}
</HTML>

<T.AmbientLight intensity={isPremiumEnabled ? 1.0 : 1.5} />
<T.DirectionalLight position={[10, 10, 10]} intensity={5} castShadow />
<T.DirectionalLight position={[-10, 5, -10]} intensity={3} color="#4287f5" />
<T.HemisphereLight intensity={1.0} groundColor="#444444" skyColor="#ffffff" />

<Stars />
{#if isPremiumEnabled}
	<ScenePremiumEffects />
{/if}

{#if isBloomEnabled}
	<Bloom />
{/if}

{#if geometries.length > 0}
	{#each geometries as geometry (geometry.id)}
		{#if geometry && geometry.visible}
			{@const isTransformed =
				transformSettings.enabled && transformSettings.selectedId == geometry.id}

			{#if typeof window !== 'undefined'}
				<Float floatIntensity={isTransformed ? 0 : 1} floatingRange={[0, 1]}>
					<Dynamic3DModel
						{geometry}
						bind:ref={modelRefs[geometry.id]}
						onPointerDown={() => {
							if (transformSettings.selectedId !== geometry.id) {
								transformSettings.selectedId = geometry.id;
								// Inform form about selection
								window.dispatchEvent(
									new CustomEvent('manualTransformSync', {
										detail: {
											id: geometry.id,
											position: geometry.position,
											rotation: geometry.rotation,
											scale: geometry.scale
										}
									})
								);
							}
						}}
					/>
				</Float>

				{#if transformSettings.selectedId == geometry.id}
					<Outlines color="#4db6ac" />
				{/if}

				{#if isTransformed && modelRefs[geometry.id]}
					{#each transformSettings.modes as mode}
						<TransformControls
							object={modelRefs[geometry.id]}
							{mode}
							onstart={() => window.dispatchEvent(new CustomEvent('lockCamera'))}
							onend={() => {
								window.dispatchEvent(new CustomEvent('unlockCamera'));
								window.dispatchEvent(
									new CustomEvent('manualTransformSync', {
										detail: {
											id: geometry.id,
											position: geometry.position,
											rotation: geometry.rotation,
											scale: geometry.scale,
											save: true
										}
									})
								);
							}}
							onchange={() => syncGeometry(geometry, modelRefs[geometry.id])}
						/>
					{/each}
				{/if}
			{:else}
				<Dynamic3DModel {geometry} />
			{/if}
		{/if}
	{/each}
{/if}

<style>
	.scene-label {
		color: #4db6ac;
		font-family: monospace;
		font-weight: bold;
		opacity: 0.5;
		pointer-events: none;
	}

	.error,
	.loading,
	.empty {
		color: white;
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		background: rgba(0, 0, 0, 0.7);
		padding: 1rem;
		border-radius: 8px;
		z-index: 100;
	}
</style>
