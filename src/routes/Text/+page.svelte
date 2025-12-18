<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Scene from './scene.svelte';

	let { data } = $props();
</script>

<Canvas renderMode="always">
	<T.PerspectiveCamera makeDefault position={[0, 0, 15]} fov={60}>
		<OrbitControls enableDamping enableZoom enableRotate enablePan />
	</T.PerspectiveCamera>
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[10, 10, 5]} intensity={1} />
	<Scene />
</Canvas>
