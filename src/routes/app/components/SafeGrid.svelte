<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { Grid } from '@threlte/extras';
	import { onMount } from 'svelte';

	let { ...props } = $props();
	const { camera } = useThrelte();

	let ready = $state(false);

	onMount(() => {
		// Wait one frame to ensure camera is Default and fully registered
		const timeout = setTimeout(() => {
			if ($camera) ready = true;
		}, 100);
		return () => clearTimeout(timeout);
	});
</script>

{#if ready && $camera}
	<Grid {...props} />
{/if}
