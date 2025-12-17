<script lang="ts">
	import { T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Vaguend from './vaguend.svelte';
	import About from '../stores/About.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let Canvas: any;

	let {
		position = [0, 0, 0],
		rotation = [0, 0, 0],
		scale = 0.8
	}: {
		position?: [number, number, number];
		rotation?: [number, number, number];
		scale?: number | [number, number, number];
	} = $props();

	onMount(async () => {
		if (browser) {
			const threlte = await import('@threlte/core');
			Canvas = threlte.Canvas;
		}
	});
</script>

{#if browser && Canvas}
	<Canvas>
		<T.PerspectiveCamera makeDefault position={[10, 10, 10]}>
			<OrbitControls enableDamping enableZoom enableRotate enablePan />
		</T.PerspectiveCamera>
		<T.AmbientLight intensity={0.5} />
		<T.DirectionalLight position={[5, 10, 5]} intensity={1} />
		<Vaguend {position} {rotation} {scale} />
		<About />
	</Canvas>
{/if}
