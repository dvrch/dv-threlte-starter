<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { Group } from 'three';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';

	// Runes syntax pour les props
	let { ref = new Group(), ...restProps } = $props();

	let gltf: any;
	let map: any;

	onMount(() => {
		if (browser) {
			gltf = useGltf(getCloudinaryAssetUrl('/models/spaceship.glb'));
			map = useTexture(getCloudinaryAssetUrl('/textures/energy-beam-opacity.png'));
		}
	});
	gltf?.then(() => {
		// Point d'extension si tu veux faire des ajustements sur les matériaux plus tard
	});
</script>

<T is={ref} dispose={false} {...restProps}>
	{#await gltf}
		loading
	{:then gltf}
		<T.Mesh is={gltf.scene} />
	{:catch error}
		<p>Error loading model</p>
	{/await}

	<slot {ref} />
</T>
