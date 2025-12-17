<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import { onMount } from 'svelte';
	import * as THREE from 'three';

	let meshRef: THREE.Mesh;

	onMount(() => {
		// Créer une géométrie simple avec une rotation continue
		const geometry = new THREE.BoxGeometry(2, 2, 2);
		const material = new THREE.MeshStandardMaterial({ color: '#4169E1' });
		const mesh = new THREE.Mesh(geometry, material);

		// Animation de rotation sur l'axe Z
		setInterval(() => {
			mesh.rotation.z += 0.01;
		}, 16);
	});

	function addRandomCube() {
		const geometry = new THREE.BoxGeometry(1, 1, 1);
		const material = new THREE.MeshStandardMaterial({
			color: `hsl(${Math.random() * 360}, 70%, 50%)`
		});
		const mesh = new THREE.Mesh(geometry, material);

		// Position aléatoire dans un espace plus grand
		mesh.position.set((Math.random() - 0.5) * 20, Math.random() * 10, (Math.random() - 0.5) * 20);

		return mesh;
	}
</script>

<Canvas>
	<T.PerspectiveCamera makeDefault position={[15, 10, 15]} fov={60}>
		<OrbitControls enableDamping enableZoom enableRotate enablePan />
	</T.PerspectiveCamera>

	<T.AmbientLight intensity={0.3} />
	<T.DirectionalLight position={[10, 10, 5]} intensity={1} castShadow />

	<!-- Sol -->
	<T.Mesh position={[0, -1, 0]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
		<T.PlaneGeometry args={[50, 50]} />
		<T.MeshStandardMaterial color="#f0f0f0" />
	</T.Mesh>

	<!-- Grille -->
	<T.GridHelper args={[25, 25]} position={[0, -0.99, 0]} />

	<!-- Plusieurs objets rotatifs pour créer l'effet ZNE -->
	{#each Array.from({ length: 20 }) as _, i}
		<T.Mesh position={[Math.cos(i * 0.3) * 8, 2, Math.sin(i * 0.3) * 8]} let:ref castShadow>
			<T.BoxGeometry args={[1.5, 1.5, 1.5]} />
			<T.MeshStandardMaterial color={`hsl(${i * 18}, 80%, 60%)`} />
		</T.Mesh>
	{/each}
</Canvas>

<style>
	:global(body) {
		margin: 0;
		overflow: hidden;
		background: #000;
	}
</style>
