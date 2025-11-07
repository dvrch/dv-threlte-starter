<script lang="ts">
	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Vaguend from './vaguend.svelte';
	import About from '../stores/About.svelte';

	export let position: [number, number, number] = [0, 0, 0];
	export let rotation: [number, number, number] = [0, 0, 0];
	export let scale: number | [number, number, number] = 0.8;
	export let data;
	export let params = {};
</script>

<Vaguend {position} {rotation} {scale} />

<!-- <Canvas>
	<About />
</Canvas> -->
