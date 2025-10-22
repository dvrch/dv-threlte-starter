<script>
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import { degToRad } from 'three/src/math/MathUtils';

	console.log('Scene 3D page initialized');
</script>

<div>
	<Canvas>
		<T.PerspectiveCamera makeDefault position={[10, 10, 10]} fov={24}>
			<OrbitControls />
		</T.PerspectiveCamera>

		<T.DirectionalLight castShadow position={[3, 10, 10]} />
		<T.DirectionalLight position={[-3, 10, -10]} intensity={0.2} />
		<T.AmbientLight intensity={0.2} />

		<!-- Cube -->
		<T.Group>
			<T.Mesh position.y={0.5} castShadow>
				<T.BoxGeometry />
				<T.MeshStandardMaterial color="#333333" />
			</T.Mesh>
		</T.Group>

		<!-- Floor -->
		<T.Mesh receiveShadow rotation.x={degToRad(-90)}>
			<T.CircleGeometry args={[3, 72]} />
			<T.MeshStandardMaterial color="white" />
		</T.Mesh>
	</Canvas>
</div>

<style>
	div {
		height: 100vh;
		width: 100vw;
	}
</style>