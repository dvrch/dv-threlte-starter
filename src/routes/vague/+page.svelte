<script lang="ts">
	import { T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Vaguend from './vaguend.svelte';
	import About from '../stores/About.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let Canvas;

	let { position, rotation, scale } = $props<{
		position?: [number, number, number];
		rotation?: [number, number, number];
		scale?: number | [number, number, number];
	}>({
		position: [0, 0, 0],
		rotation: [0, 0, 0],
		scale: 0.8
	});

	onMount(async () => {
		if (browser) {
			const threlte = await import('@threlte/core');
			Canvas = threlte.Canvas;
		}
	});
</script>

<Vaguend {position} {rotation} {scale} />

{#if browser && Canvas}
	<Canvas>
		<About />
	</Canvas>
{/if}
