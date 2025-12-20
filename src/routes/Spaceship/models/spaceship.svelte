<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { Group } from 'three';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { createDracoLoader } from '$lib/utils/draco-loader';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfUrl = $state<string | null>(null);
	let mapUrl = $state<string | null>(null);

	onMount(async () => {
		if (browser) {
			gltfUrl = await getWorkingAssetUrl('spaceship.glb', 'models');
			mapUrl = await getWorkingAssetUrl('energy-beam-opacity.png', 'textures');
		}
	});

	// Use derived stores for the results
	const gltf = $derived(gltfUrl ? useGltf(gltfUrl, { dracoLoader: createDracoLoader() }) : null);
	const map = $derived(mapUrl ? useTexture(mapUrl) : null);
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltf}
		{#await gltf then value}
			<T.Group scale={0.01}>
				<T is={value.scene} />
			</T.Group>
		{/await}
	{:else}
		<slot name="fallback" />
	{/if}

	<slot {ref} />
</T>
