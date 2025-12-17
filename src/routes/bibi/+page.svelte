<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Demo_09 from './demo_09.svelte';

	let { data, params } = $props();
</script>

<Canvas>
	<T.PerspectiveCamera makeDefault position={[5, 5, 5]}>
		<OrbitControls enableDamping enableZoom enableRotate enablePan />
	</T.PerspectiveCamera>
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[10, 10, 0]} intensity={1} />
	<Demo_09 />
</Canvas>

<!-- <script lang="ts">
import { Canvas } from '@threlte/core';
import Demo_09 from './demo_09.svelte'; // Assurez-vous que le chemin est correct
</script>

<Canvas>
  <Demo_09 />
</Canvas> -->

<style>
	:global(body) {
		margin: 0;
		overflow: hidden;
	}
</style>
