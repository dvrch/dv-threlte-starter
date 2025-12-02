<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	export let url: string;

	let gltf: any; // Declare gltf as a mutable variable

	onMount(() => {
		if (browser) {
			gltf = useGltf(url); // Call useGltf only on the client
		}
	});
</script>

{#if browser && gltf}
	<T is={gltf.scene} {...$restProps} />
{:else}
	<!-- Fallback for SSR, maybe a placeholder or nothing -->	<T.Group />
{/if}