<script lang="ts">
	import { browser } from '$app/environment';
	import { getModelUrlByName } from '$lib/utils/geometry-loader';

	let {
		geometryName,
		fallbackUrl,
		component: Component,
		...restProps
	}: {
		geometryName: string;
		fallbackUrl?: string;
		component: any;
		[key: string]: any;
	} = $props();

	let modelUrl = $state<string | null>(null);
	let isLoading = $state(true);

	// Find model URL from API
	getModelUrlByName(geometryName)
		.then((url) => {
			modelUrl = url || fallbackUrl || null;
			isLoading = false;
		})
		.catch((err) => {
			console.error(`Failed to load ${geometryName} model:`, err);
			modelUrl = fallbackUrl || null;
			isLoading = false;
		});
</script>

{#if browser && modelUrl}
	<svelte:component this={Component} url={modelUrl} {...restProps} />
{:else if isLoading}
	<!-- Loading placeholder -->
	<div class="loading-placeholder">Loading {geometryName}...</div>
{:else}
	<!-- Error fallback -->
	<div class="error-placeholder">Failed to load {geometryName}</div>
{/if}
