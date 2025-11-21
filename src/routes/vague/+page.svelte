<script lang="ts">
	import { T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Vaguend from './vaguend.svelte';
	import About from '../stores/About.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let Canvas;

	export let position: [number, number, number] = [0, 0, 0];
	export let rotation: [number, number, number] = [0, 0, 0];
	export let scale: number | [number, number, number] = 0.8;

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
