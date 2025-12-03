<script lang="ts">
	import { T } from '@threlte/core';
	import { Float, Grid } from '@threlte/extras';
	import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
	import { browser } from '$app/environment';

	let { data } = $props();
	const { geometries, error } = data;
</script>

{#if error}
	<p class="error">Erreur: {error}</p>
{:else if !geometries}
	<p class="loading">Chargement des géométries...</p>
{:else if geometries.length === 0}
	<p class="empty">Aucune géométrie trouvée</p>
{:else}
	<Grid />

	<!-- Sphère au centre -->
	<T.Mesh position={[0, 0.5, 0]}>
		<T.SphereGeometry args={[0.5, 32, 32]} />
		<T.MeshStandardMaterial color="red" />
	</T.Mesh>

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
