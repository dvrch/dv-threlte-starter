<script lang="ts">
	import Nissan from '../Spaceship/Nissan.svelte'
	import { T } from '@threlte/core'
	import { Grid, OrbitControls, TransformControls } from '@threlte/extras'
	import * as Three from 'three'
	const { DEG2RAD } = Three.MathUtils
	import { onMount } from 'svelte';


	let nissanPosition = { x: 0, y: 4, z: 0 };
	const speed = 0.1;

	onMount(() => {
		window.addEventListener('keydown', handleKeyDown);
		return () => {
			window.removeEventListener('keydown', handleKeyDown);
		};
	});

	function handleKeyDown(event: KeyboardEvent) {
		switch (event.key) {
			case 'ArrowLeft':
				nissanPosition.x -= speed;
				break;
			case 'ArrowRight':
				nissanPosition.x += speed;
				break;
			case 'ArrowUp':
				nissanPosition.z -= speed;
				break;
			case 'ArrowDown':
				nissanPosition.z += speed;
				break;
		}
	}
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
<Nissan position={[nissanPosition.x, nissanPosition.y, nissanPosition.z]} let:ref castShadow>
	<TransformControls object={ref} />
</Nissan>

<!-- Sphere -->
<!-- <T.Mesh position={[0, 4, 0]} let:ref castShadow>
	<T.SphereGeometry args={[4, 64, 64]} />
	<T.MeshStandardMaterial color="white" />
	<TransformControls object={ref} />
</T.Mesh> -->

<!-- Floor -->
<T.Mesh rotation.x={DEG2RAD * 90} receiveShadow>
	<T.PlaneGeometry args={[20, 20]} />
	<T.MeshStandardMaterial color="white" side={Three.DoubleSide} />
</T.Mesh>

