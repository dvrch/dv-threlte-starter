<script lang="ts">
	export let data;
	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	//import Bibanime from './bibanime.svelte';

	import TissusSimulat from './tissus-simulat.svelte';
	// import TissusSimulat from './demo_01.svelte';
	
	const defaultPosition: [number, number, number] = [2, 2, 2];
	const defaultRotation: [number, number, number] = [0, 0, 0];
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
	<TissusSimulat position={defaultPosition} rotation={defaultRotation} />
</Canvas>
