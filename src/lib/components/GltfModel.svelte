<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useGltfAnimations } from '@threlte/extras';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';

	// Receive URL and other props
	let { url, ...restProps }: { url: string; [key: string]: any } = $props();

	let resolvedUrl = $state('');

	// Load GLTF at the top level with reactive URL support
	const gltf = useGltf(() => resolvedUrl, {
		dracoLoader: createDracoLoader()
	});

	// useGltfAnimations extracts animations and provides 'actions'.
	const { actions } = useGltfAnimations(gltf);

	onMount(async () => {
		if (browser && url) {
			// Extract filename from URL (which might be a full Cloudinary URL or just a name)
			const filename = url.split('/').pop() || url;
			// Pass 'models' as target folder to look into /models/ if local fallback is needed
			resolvedUrl = await getWorkingAssetUrl(filename, 'models');
		}
	});

	// Effect to play animations once they are loaded
	$effect(() => {
		if ($actions) {
			Object.values($actions).forEach((action) => {
				action?.reset().play();
			});
		}
	});
</script>

{#if browser && $gltf}
	<T is={$gltf.scene} {...restProps} />
{:else}
	<T.Group />
{/if}
