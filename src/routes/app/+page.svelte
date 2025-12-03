<script lang="ts">
	import { T } from '@threlte/core';
	import { Float, Grid } from '@threlte/extras';
	import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { PUBLIC_API_URL } from '$env/static/public';

	let geometries = $state([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

	onMount(async () => {
		try {
			const apiUrl = PUBLIC_API_URL 
				? `${PUBLIC_API_URL}/api/geometries/` 
				: '/api/geometries/';
			
			const response = await fetch(apiUrl);
			if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
			
			const data = await response.json();
			geometries = data.results || [];
			console.log('Loaded geometries:', geometries.length);
		} catch (e) {
			error = (e as Error).message;
			console.error('Error loading geometries:', e);
		} finally {
			loading = false;
		}
	});
</script>

{#if error}
	<p class="error">Erreur: {error}</p>
{:else if loading}
	<p class="loading">Chargement des géométries...</p>
{:else if geometries.length === 0}
	<p class="empty">Aucune géométrie trouvée</p>
{/if}

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
