<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { dracoGltfLoader } from '$lib/utils/cloudinaryAssets';

	let { url, ...restProps }: { url: string } = $props();

	let gltf: any = $state(null); // Declare gltf as a mutable variable
	
	$effect(() => {
		if (browser && url) {
			const gltfStore = useGltf(url, { loader: dracoGltfLoader });
			// useGltf return a store that is also a promise
			gltfStore.then((loaded) => {
				gltf = loaded;
			}).catch((err) => {
				console.error("Failed to load GLTF:", url, err);
				gltf = null;
			});
		}
	});
</script>

{#if browser && gltf}
	<T is={gltf.scene} {...restProps} />
{:else}
	<!-- Fallback for SSR, maybe a placeholder or nothing -->	<T.Group />
{/if}