<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { Group } from 'three';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';

	import { createDracoLoader } from '$lib/utils/draco-loader';

	// Runes syntax pour les props
	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltf = $state<any>(null);
	let map: any;

	onMount(() => {
		if (browser) {
			const loadGltf = async () => {
				try {
					return await useGltf(getCloudinaryAssetUrl('spaceship.glb'), {
						dracoLoader: createDracoLoader()
					});
				} catch (e) {
					console.warn('Spaceship: Cloudinary fail, trying local...');
					return await useGltf('/models/spaceship.glb', {
						dracoLoader: createDracoLoader()
					});
				}
			};

			loadGltf()
				.then((data) => {
					gltf = data;
				})
				.catch((err) => console.error('Spaceship load error:', err));

			const loadTexture = async () => {
				try {
					return await useTexture(getCloudinaryAssetUrl('energy-beam-opacity.png'));
				} catch (e) {
					return await useTexture('/textures/energy-beam-opacity.png');
				}
			};
			loadTexture().then((t) => (map = t));
		}
	});
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltf}
		<T.Group scale={0.01}>
			<T is={gltf.scene} />
		</T.Group>
	{:else}
		<slot name="fallback" />
	{/if}

	<slot {ref} />
</T>
