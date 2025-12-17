<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Vaguend from './vaguend.svelte';
	import About from '../stores/About.svelte';

	let {
		position = [0, 0, 0],
		rotation = [0, 0, 0],
		scale = 0.8
	}: {
		position?: [number, number, number];
		rotation?: [number, number, number];
		scale?: number | [number, number, number];
	} = $props();
</script>

<Canvas>
	<T.PerspectiveCamera makeDefault position={[10, 10, 10]}>
		<OrbitControls enableDamping enableZoom enableRotate enablePan />
	</T.PerspectiveCamera>
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[5, 10, 5]} intensity={1} />
	<Vaguend {position} {rotation} {scale} />
	<About />
</Canvas>
