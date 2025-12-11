<script lang="ts">
	import { T } from '@threlte/core';
	import { Float, Grid, HTML } from '@threlte/extras';
	import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { ENDPOINTS } from '$lib/config';

	let geometries = $state([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

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
				if (g.type === 'gltf_model' || g.type === 'glb') {
					return g.model_url && g.model_url.trim() !== '';
				}
				return true;
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

	onMount(async () => {
		fetchGeometries();
		window.addEventListener('modelAdded', fetchGeometries);
		return () => {
			window.removeEventListener('modelAdded', fetchGeometries);
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

{#if geometries.length > 0}
	{#each geometries as geometry (geometry.id)}
		{#if browser}
			<Float floatIntensity={1} floatingRange={[0, 1]}>
				<Dynamic3DModel {geometry} />
			</Float>
		{:else}
			<!-- Fallback for SSR -->
			<Dynamic3DModel {geometry} />
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
