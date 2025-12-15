<script lang="ts">
	import { T } from '@threlte/core';
	import { Float, Grid, HTML } from '@threlte/extras';
	import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { ENDPOINTS } from '$lib/config';

	interface GeometryItem {
		id: string;
		name: string;
		type: string;
		color: string;
		position: { x: number; y: number; z: number };
		rotation: { x: number; y: number; z: number };
		visible: boolean; // Add visible property
		model_url?: string; // Assuming this exists for gltf_model types
	}

	let geometries = $state<GeometryItem[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let isBloomEnabled = $state(false); // State to control Bloom effect

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
			geometries = results
				.filter((g: any) => {
					if (g.type === 'gltf_model' || g.type === 'glb') {
						return g.model_url && g.model_url.trim() !== '';
					}
					return true;
				})
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

	onMount(async () => {
		fetchGeometries();
		window.addEventListener('modelAdded', fetchGeometries);

		const handleVisibilityChange = async (event: CustomEvent) => {
			const { id } = event.detail;
			try {
				const response = await fetch(`${ENDPOINTS.GEOMETRIES}${id}/toggle-visibility/`, {
					method: 'PATCH'
				});
				if (!response.ok) {
					throw new Error('Failed to toggle visibility');
				}
				const updatedGeometry = await response.json();
				geometries = geometries.map((g) =>
					g.id === updatedGeometry.id ? { ...g, visible: updatedGeometry.visible } : g
				);
			} catch (err) {
				console.error('Error toggling visibility:', err);
				// Optionally, dispatch an event to show a toast notification
			}
		};
		window.addEventListener('geometryVisibilityChanged', handleVisibilityChange);

		const handleToggleBloom = (event: CustomEvent) => {
			isBloomEnabled = event.detail.enabled;
		};
		window.addEventListener('toggleBloomEffect', handleToggleBloom);

		return () => {
			window.removeEventListener('modelAdded', fetchGeometries);
			window.removeEventListener('geometryVisibilityChanged', handleVisibilityChange);
			window.removeEventListener('toggleBloomEffect', handleToggleBloom);
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

<Grid />

<!-- Sphère au centre -->
<T.Mesh position={[0, 0.5, 0]}>
	<T.SphereGeometry args={[0.5, 32, 32]} />
	<T.MeshStandardMaterial color="red" />
</T.Mesh>

{#if isBloomEnabled}
	<BloomEffect />
{/if}

{#if geometries.length > 0}
	{#each geometries as geometry (geometry.id)}
		{#if geometry.visible}
			{#if browser}
				<Float floatIntensity={1} floatingRange={[0, 1]}>
					<Dynamic3DModel {geometry} />
				</Float>
			{:else}
				<!-- Fallback for SSR -->
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
