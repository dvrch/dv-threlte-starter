<script>
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras'; // Réactivé
	import { degToRad } from 'three/src/math/MathUtils';
	import { tweened } from 'svelte/motion';
	import InteractivitySetup from '$lib/InteractivitySetup.svelte';

	const zoom = tweened(1, { duration: 250 });
</script>

<div>
	<Canvas>
		<InteractivitySetup />
		<T.PerspectiveCamera makeDefault position={[10, 10, 10]} fov={24} zoom={$zoom}>
			<OrbitControls maxPolarAngle={degToRad(80)} enableZoom={false} target={{ y: 0.5 }} />
		</T.PerspectiveCamera>

		<T.DirectionalLight castShadow position={[3, 10, 10]} />
		<T.DirectionalLight position={[-3, 10, -10]} intensity={0.2} />
		<T.AmbientLight intensity={0.2} />

		<!-- Cube -->
		<T.Group>
			<T.Mesh
				position.y={0.5}
				castShadow
				on:pointerenter={() => zoom.set(1.5)}
				on:pointerleave={() => zoom.set(1)}
			>
				<T.BoxGeometry />
				<T.MeshStandardMaterial color="#333333" />
			</T.Mesh>
		</T.Group>

		<!-- Floor -->
		<T.Mesh receiveShadow rotation.x={degToRad(-90)}>
			<T.CircleGeometry args={[3, 72]} />
			<T.MeshStandardMaterial color="white" />		</T.Mesh>
	</Canvas>
</div>

<style>
	div {
		height: 100vh;
		width: 100vw;
	}
</style>