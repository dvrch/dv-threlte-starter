<script lang="ts">
	
	import { T, Canvas } from '@threlte/core'
	import { OrbitControls } from '@threlte/extras'
	import * as THREE from 'three'
	import { onMount, onDestroy, createEventDispatcher } from 'svelte';

	let canvas: HTMLCanvasElement;
	let vagueMesh: THREE.Points;
	let scene: THREE.Scene;
	let camera: THREE.PerspectiveCamera;
	let renderer: THREE.WebGLRenderer;
	const dispatch = createEventDispatcher();

	export let position: [number, number, number];
	export let rotation: [number, number, number];
	export let scale: number | [number, number, number];

	// Assurons-nous que scaleArray est toujours un tuple de 3 éléments
	$: scaleArray = Array.isArray(scale) ? scale : [scale, scale, scale] as [number, number, number];
	export let width = 100;
	export let height = 100;

	onMount(() => {
		scene = new THREE.Scene();
		camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight);
		const geometry = computeGeometry();
		const material = new THREE.PointsMaterial({ size: 0.015, vertexColors: true });
		vagueMesh = new THREE.Points(geometry, material);

		scene.add(vagueMesh);

		camera.position.set(0, 1, 2);
		camera.lookAt(0, -0.5, 0);

		renderer = new THREE.WebGLRenderer({ canvas });
		renderer.setSize(window.innerWidth, window.innerHeight);
		renderer.setClearColor(0x000000, 1);

		const clock = new THREE.Clock();
		let t = 0;

		function loop() {
			t += clock.getDelta();
			animeGeometry(geometry, t);
			vagueMesh.rotation.y = 0.1 * t;
			renderer.render(scene, camera);
			dispatch('render', { scene, camera, renderer });
			requestAnimationFrame(loop);
		}

		loop();
	});

	onDestroy(() => {
		// Nettoyage si nécessaire
		renderer.dispose(); // Libération des ressources du renderer
	});

	function computeGeometry(): THREE.BufferGeometry {
		const space = 4, nb = 100, amp = 0.1, pi2 = Math.PI * 2;
		const geometry = new THREE.BufferGeometry();
		const positions = new Float32Array(nb * nb * 3);
		const colors = new Float32Array(nb * nb * 3);
		let k = 0;

		for (let i = 0; i < nb; i++) {
			for (let j = 0; j < nb; j++) {
				const x = i * (space / nb) - space / 2;
				const z = j * (space / nb) - space / 2;
				const y = amp * (Math.cos(x * pi2) + Math.sin(z * pi2));
				positions[3 * k + 0] = x;
				positions[3 * k + 1] = y;
				positions[3 * k + 2] = z;
				const intensity = (y / amp) / 2 + 0.3;
				colors[3 * k + 0] = j / nb * intensity;
				colors[3 * k + 1] = 0;
				colors[3 * k + 2] = i / nb * intensity;
				k++;
			}
		}
		geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
		geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
		geometry.computeBoundingBox();
		return geometry;
	}

	function animeGeometry(geometry: THREE.BufferGeometry, progress: number): void {
		const space = 4, nb = 100, amp = 0.1, pi2 = Math.PI * 2;
		const phase = progress;
		const fre = 0.8 + Math.cos(progress) / 2;

		let k = 0;
		for (let i = 0; i < nb; i++) {
			for (let j = 0; j < nb; j++) {
				const x = i * (space / nb) - space / 2;
				const z = j * (space / nb) - space / 2;
				const y = amp * (Math.cos(x * pi2 * fre + phase) + Math.sin(z * pi2 * fre + phase));
				geometry.attributes.position.setY(k, y);
				const intensity = (y / amp) / 2 + 0.3;
				geometry.attributes.color.setX(k, j / nb * intensity);
				geometry.attributes.color.setZ(k, i / nb * intensity);
				k++;
			}
		}
		geometry.attributes.position.needsUpdate = true;
		geometry.attributes.color.needsUpdate = true;
	}


</script>

<div class="scene-container">
	<T.Group 
		position={position} 
		rotation={rotation} 
		scale={scaleArray}
		matrixAutoUpdate={true}
	>
		<Canvas>
			<T.PerspectiveCamera makeDefault position={[0, 5, 10]} fov={75}>
				<OrbitControls />
			</T.PerspectiveCamera>

			<T.Scene>
				{#if vagueMesh}
					<T is={vagueMesh} />
				{/if}
			</T.Scene>
		</Canvas>

		<div class="vague-container">
			<canvas bind:this={canvas} {width} {height}></canvas>
		</div>
	</T.Group>
</div>

<style>
	.scene-container {
		position: relative;
		width: 100%;
		height: 100vh;
	}

	.vague-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: -2;
		transform: scale(1.2);
		transition: transform 0.5s ease;
	}

	canvas {
		width: 100%;
		height: 100%;
	}

	:global(*) {
		margin: 0;
		padding: 0;
		overflow: hidden;
	}
</style>
