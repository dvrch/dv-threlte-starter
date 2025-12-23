<script lang="ts">
	import { T } from '@threlte/core';
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
	import { ENDPOINTS } from '$lib/config';
	import { Group } from 'three';

	import { addToast } from '$lib/stores/toasts';
	import Bloom from './models/bloom.svelte';
	import Stars from '../Spaceship/Stars.svelte';
	import ScenePremiumEffects from './components/ScenePremiumEffects.svelte';
	import SceneText2 from '../Text/scene.svelte';

	interface GeometryItem {
		id: string;
		name: string;
		type: string;
		color: string;
		position: { x: number; y: number; z: number };
		rotation: { x: number; y: number; z: number };
		scale: { x: number; y: number; z: number };
		visible: boolean; // Add visible property
		model_url?: string; // Assuming this exists for gltf_model types
	}

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

	onMount(() => {
		fetchGeometries();
		window.addEventListener('modelAdded', fetchGeometries);

		// ... listeners ...

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
		// ...
		return () => {
			// ...
			window.removeEventListener('togglePremiumEffect', handleTogglePremium);
		};
	});

	// Store for model refs
	let modelRefs = $state<Record<string, Group>>({});

	const syncGeometry = (geometry: GeometryItem, obj: Group) => {
		if (obj && geometry) {
			geometry.position = { x: obj.position.x, y: obj.position.y, z: obj.position.z };
			geometry.rotation = {
				x: obj.rotation.x * (180 / Math.PI),
				y: obj.rotation.y * (180 / Math.PI),
				z: obj.rotation.z * (180 / Math.PI)
			};
			geometry.scale = { x: obj.scale.x, y: obj.scale.y, z: obj.scale.z };

			// Sync form real-time during move
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

	// Function to fetch geometries
	const fetchGeometries = async () => {
		try {
			const apiUrl = ENDPOINTS.GEOMETRIES;
			console.log('Fetching geometries from:', apiUrl);
			const response = await fetch(apiUrl);

			if (!response.ok) {
				const errorText = await response.text();
				console.error('API Error Response:', errorText);
				throw new Error(`HTTP error! status: ${response.status} - ${errorText.substring(0, 200)}`);
			}

			const data = await response.json();
			const results = Array.isArray(data) ? data : data.results || [];
			// Filter out geometries that expect an URL but have none
			geometries = results.filter((g: any) => {
				if (g.model_type === 'gltf' || g.model_type === 'glb') {
					return g.model_url && g.model_url.trim() !== '';
				}
				return true;
			});

			// Pre-initialize model refs to ensure stability
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

		// Debug: log final state
		console.log('Final state:', { loading, error, geometriesCount: geometries.length });
	};

	onMount(() => {
		fetchGeometries();
		window.addEventListener('modelAdded', fetchGeometries);

		const handleVisibilityChange = (event: Event) => {
			const customEvent = event as CustomEvent;
			const { id, visible } = customEvent.detail; // 'visible' is the NEW desired state
			if (typeof visible !== 'boolean') return; // Safety check

			// Update local state without calling API (AddGeometry handles the API call)
			geometries = geometries.map((g) => (g.id == id ? { ...g, visible: visible } : g));
		};
		window.addEventListener('geometryVisibilityChanged', handleVisibilityChange);

		const handleToggleBloom = (event: Event) => {
			const customEvent = event as CustomEvent;
			isBloomEnabled = customEvent.detail.enabled;
		};
		window.addEventListener('toggleBloomEffect', handleToggleBloom);

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
			window.removeEventListener('toggleTransformControls', handleToggleTransform);
		};
	});
</script>

<HTML center>
	{#if error}
		<p class="error">Erreur: {error}</p>
	{:else if loading}
		<p class="loading">Chargement des géométries...</p>
	{:else if geometries.length === 0}
		<p class="empty">Aucune géométrie trouvée</p>
	{/if}
</HTML>

<T.AmbientLight intensity={isPremiumEnabled ? 1.0 : 1.5} />
<T.DirectionalLight position={[10, 10, 10]} intensity={5} castShadow />
<T.DirectionalLight position={[-10, 5, -10]} intensity={3} color="#4287f5" />
<T.HemisphereLight intensity={1.0} groundColor="#444444" skyColor="#ffffff" />

<Stars />
<SceneText2 />
{#if isPremiumEnabled}
	<ScenePremiumEffects />
{/if}

<!-- Sphère au centre -->
<T.Mesh position={[0, 0.5, 0]}>
	<T.SphereGeometry args={[0.5, 32, 32]} />
	<T.MeshStandardMaterial color="red" emissive="red" emissiveIntensity={2} />
</T.Mesh>

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
