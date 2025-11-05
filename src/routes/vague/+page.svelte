<script lang="ts">
	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Vaguend from './vaguend.svelte';
	import About from '../stores/About.svelte';

	export let position: [number, number, number] = [0, 0, 0];
	export let rotation: [number, number, number] = [0, 0, 0];
	export let scale: number | [number, number, number] = 0.8;
</script>

<Canvas>
	<T.PerspectiveCamera 
	makeDefault 
	position={[0, 5, 10]} 
	fov={75}
	>
	<OrbitControls 
	enableDamping={true}
	dampingFactor={0.05}
	autoRotate={true}
				autoRotateSpeed={1}
				maxDistance={20}
				minDistance={2}
		/>
	</T.PerspectiveCamera>
	
	<Vaguend {position} {rotation} {scale} />
</Canvas>

<!-- <Canvas>
	<About />
</Canvas> -->
