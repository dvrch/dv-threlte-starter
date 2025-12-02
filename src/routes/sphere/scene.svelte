<script lang="ts">
	import Nissan from '../Spaceship/Nissan.svelte'
	import { T } from '@threlte/core'
	import { Grid, OrbitControls, TransformControls } from '@threlte/extras'
	import * as Three from 'three'
	const { DEG2RAD } = Three.MathUtils
	import { onMount } from 'svelte';

	// Créer une courbe fermée
	const curve = new Three.CatmullRomCurve3([
		new Three.Vector3(-5, 0, 5),
		new Three.Vector3(0, 0, 5),
		new Three.Vector3(5, 0, 5),
		new Three.Vector3(5, 0, 0),
		new Three.Vector3(5, 0, -5),
		new Three.Vector3(0, 0, -5),
		new Three.Vector3(-5, 0, -5),
		new Three.Vector3(-5, 0, 0),
	], true);

	let curvePosition = 0;
	const speed = 0.005;

 let nissanPosition = $derived(curve.getPoint(curvePosition));
 let nissanRotation = $derived(new Three.Euler().setFromQuaternion();
		new Three.Quaternion().setFromUnitVectors(
			new Three.Vector3(0, 0, 1),
			curve.getTangent(curvePosition)
		)
	);

	// $: {
	// 	console.log('Position Nissan:', nissanPosition);
	// 	console.log('Rotation Nissan:', nissanRotation);
	// }

	function handleKeyDown(event: KeyboardEvent) {
		switch (event.key) {
			case 'ArrowUp':
				curvePosition = (curvePosition + speed) % 1;
				break;
			case 'ArrowDown':
				curvePosition = (curvePosition - speed + 1) % 1;
				break;
		}
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeyDown);
		return () => {
			window.removeEventListener('keydown', handleKeyDown);
		};
	});
	
</script>

<!-- Grid -->
<Grid cellColor="gray" sectionSize={0} />

<!-- Camera -->
<T.PerspectiveCamera position={[20, 20, 20]} fov={50} makeDefault>
	<!-- Controls -->
	<OrbitControls enableDamping />
</T.PerspectiveCamera>

<!-- Lights the scene equally -->
<T.AmbientLight color="white" intensity={0.2} />

<!-- Light that casts a shadow -->
<T.DirectionalLight
	color="white"
	intensity={2}
	position={[10, 10, 0]}
	shadow.camera.top={8}
	castShadow
/>

<!-- Nissan -->
<Nissan position={[...nissanPosition]} rotation={[...nissanRotation]} let:ref castShadow>
	<TransformControls object={ref} />
</Nissan>


<!-- Sphere -->

<T.Mesh position={[0, 3, 2]} scale={0.3} let:ref castShadow>
	<T.SphereGeometry args={[4, 64, 64]} />
	<T.MeshStandardMaterial color="white" />
	<TransformControls object={ref} />
</T.Mesh>

<!-- Floor -->
<T.Mesh rotation.x={DEG2RAD * 90} receiveShadow>
	<T.PlaneGeometry args={[20, 20]} />
	<T.MeshStandardMaterial color="white" side={Three.DoubleSide} />
</T.Mesh>

<!-- Curve visualization -->
<T.Line position.y={0.5}>
	<T.BufferGeometry>
		{#if curve}
			<T.Float32BufferAttribute attach="attributes-position" args={[curve.getPoints(50).flatMap(v => [v.x, v.y, v.z]), 3]} />
		{/if}
	</T.BufferGeometry>
	<T.LineBasicMaterial color="red" />
</T.Line>

