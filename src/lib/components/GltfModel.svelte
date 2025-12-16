<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useGltfAnimations } from '@threlte/extras';
	import { browser } from '$app/environment';

	// Receive URL and other props
	let { url, ...restProps }: { url: string; [key: string]: any } = $props();

	// Load GLTF at the top level.
	// NOTE: This assumes the component is re-created (keyed) if the URL changes.
	const gltf = useGltf(url);

	// useGltfAnimations extracts animations and provides 'actions'.
	// It accepts the store returned by useGltf.
	const { actions } = useGltfAnimations(gltf);

	// Effect to play animations once they are loaded
	$effect(() => {
		if ($actions) {
			// Iterate over all available animations and play them
			Object.values($actions).forEach((action) => {
				action?.reset().play();
			});
		}
	});
</script>

{#if browser && $gltf}
	<!-- Render the scene from the loaded GLTF -->
	<T is={$gltf.scene} {...restProps} />
{:else}
	<!-- Fallback or empty group while loading -->
	<T.Group />
{/if}
