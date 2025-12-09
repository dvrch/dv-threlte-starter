<script lang="ts">
	
	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	// import { Canvas } from '@threlte/core';
	import Tissus from './tissus-simulat.svelte';

	const defaultPosition: [number, number, number] = [0, 0, 0];
	const defaultRotation: [number, number, number] = [0, 0, 0];
</script>

<Canvas renderMode="always">
	
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
	<Tissus position={defaultPosition} rotation={defaultRotation} />
</Canvas>
