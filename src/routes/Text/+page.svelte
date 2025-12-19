<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Scene from './scene.svelte';
	import Bloom from '../app/models/bloom.svelte';

	let { data }: { data: { cvLines: string[] } } = $props();
</script>

<div class="bg-container">
	<Canvas>
		<T.PerspectiveCamera makeDefault position={[0, 0, 12]} fov={45}>
			<OrbitControls enableDamping target={[0, 0, 0]} />
		</T.PerspectiveCamera>

		<T.Color args={['#050505']} attach="background" />
		<T.Fog args={['#050505', 10, 25]} />

		<T.AmbientLight intensity={0.2} />
		<T.DirectionalLight position={[10, 10, 5]} intensity={0.5} />

		<Scene cvLines={data.cvLines} />
	</Canvas>
</div>

<style>
	.bg-container {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background: #050505;
	}
</style>
