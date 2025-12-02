<script lang="ts">
	import Bibanime from '../bibi/bibanime.svelte';

	import { T, Canvas } from '@threlte/core'
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

	let curvePosition = Math.random();
	const speed = 0.005;

	let vagueMesh: Three.Mesh;
	let bibiScene: Three.Scene;
	let bibiCamera: Three.Camera;
	let bibiRenderer: Three.WebGLRenderer;

 let bibanimePosition = $derived(curve.getPoint(curvePosition));
 let bibanimeRotation = $derived(new Three.Euler().setFromQuaternion();
		new Three.Quaternion().setFromUnitVectors(
			new Three.Vector3(0, 0, 1),
			curve.getTangent(curvePosition)
		)
	);

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

	function handleVagueRender(event) {
		const { scene, camera, renderer } = event.detail;
		if (!vagueMesh) {
			vagueMesh = scene.children[0];
			scene.remove(vagueMesh);
		}
	}

	function handleBibiSceneInitialized(event) {
		const { scene, camera, renderer } = event.detail;
		bibiScene = scene;
		bibiCamera = camera;
		bibiRenderer = renderer;
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeyDown);
		return () => {
			window.removeEventListener('keydown', handleKeyDown);
		};
	});
</script>

<div class="scene-container">
	<T.Scene>

			<Bibanime 
				position={[bibanimePosition.x, bibanimePosition.y, bibanimePosition.z]} 
				rotation={[bibanimeRotation.x, bibanimeRotation.y, bibanimeRotation.z]} />
		
		</T.Scene>

</div>

<style>
	.scene-container {
		position: relative;
		width: 100%;
		height: 100vh;
	}
</style>
