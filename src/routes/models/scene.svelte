<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { OrbitControls, useGltf } from '@threlte/extras';
	import { AmbientLight, PointLight } from 'three'; // Importer les lumières de Three.js

	const CLOUDINARY_BASE_URL = 'https://res.cloudinary.com/drcok7moc/raw/upload';

	let y = $state(2);
	let rotation = $state(0);

	function levitate() {
		const time = Date.now() / 1000;
		const speed = 1;
		const offset = 3;
		y = Math.sin(time * speed) + offset;
		requestAnimationFrame(levitate);
	}

	useTask((_, delta) => {
		rotation += delta * 0.4;
	});

	levitate();
</script>

<!-- <Bloom /> -->

<T.OrthographicCamera position={[10, 10, 10]} zoom={40} makeDefault>
	<OrbitControls enableDamping />
</T.OrthographicCamera>

<!-- <T.AmbientLight color="#8f00ff" intensity={1} /> -->
<T.PointLight intensity={10} position={[1, 2, -4]} color="#76aac8" />

{#await useGltf(`${CLOUDINARY_BASE_URL}/assets/ghost.glb`) then ghost}
	<T is={ghost.scene} position={[0, y, 0]} scale={0.4} />
{/await}

{#await useGltf(`${CLOUDINARY_BASE_URL}/assets/garden.glb`) then garden}
	<T is={garden.scene} rotation.y={rotation} />
{/await}

{#await useGltf(`${CLOUDINARY_BASE_URL}/public/nissan2.glb`) then nissan}
	<T is={nissan.scene} position={[2, y, 1]} scale={0.4} />
{/await}
