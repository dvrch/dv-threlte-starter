<script lang="ts">
	import Bibanime from './../bibi/bibanime.svelte';
	import Nissan from './models/Nissan.svelte'
	import { T, Canvas } from '@threlte/core'
	import { Grid, OrbitControls, TransformControls } from '@threlte/extras'
	import * as Three from 'three'
	const { DEG2RAD } = Three.MathUtils
	import { onMount } from 'svelte';
	import Bloom from './models/bloom.svelte';
	// import Vague from '../vague/vague.svelte';
	// import Bibi from '../bibi/+page.svelte';


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

	$: nissanPosition = curve.getPoint(curvePosition);
	$: nissanRotation = new Three.Euler().setFromQuaternion(
		new Three.Quaternion().setFromUnitVectors(
			new Three.Vector3(0, 0, 1),
			curve.getTangent(curvePosition)
		)
	);

	$: bibanimePosition = curve.getPoint(curvePosition);
	$: bibanimeRotation = new Three.Euler().setFromQuaternion(
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
		<!-- Grid -->
		<Grid cellColor="gray" sectionSize={0} />

		<!-- Nissan -->
		<Nissan position={[...nissanPosition]} rotation={[...nissanRotation]} let:ref castShadow>
			<TransformControls object={ref} />
		</Nissan>

		<Bibanime 
			position={[bibanimePosition.x, bibanimePosition.y, bibanimePosition.z]} 
			rotation={[bibanimeRotation.x, bibanimeRotation.y, bibanimeRotation.z]} />



		<!-- Curve visualization -->
		 
		   <T.Points position.y={0.5}>
            <T.BufferGeometry>
                {#if curve}
                    <T.Float32BufferAttribute attach="attributes-position" 
                    args={[curve.getPoints(50).flatMap(v => [v.x, v.y, v.z]), 3]} />
                {/if}
            </T.BufferGeometry>
            <T.PointsMaterial size={0.03} color="#00ff00" />
        </T.Points>

        <!-- <T.Line position.y={0.5}>
            <T.BufferGeometry>
                {#if curve}
                    <T.Float32BufferAttribute attach="attributes-position" 
                    args={[curve.getPoints(50).flatMap(v => [v.x, v.y, v.z]), 3]} />
                {/if}
            </T.BufferGeometry>
            <T.LineBasicMaterial color="#ff0000" linewidth={3} />
        </T.Line> -->
		
		<T.Mesh position.y={0.5}>
			{#if curve}
				<T.TubeGeometry args={[curve, 50, 0.02, 8, false]} />
				<T.MeshStandardMaterial color="red" />
			{/if}
		</T.Mesh>

		<!-- {#if vagueMesh}
			<T is={vagueMesh} />
		{/if} -->

		<!-- {#if bibiScene}
			<T is={bibiScene} />
		{/if} -->
	</T.Scene>

	 <!-- <div class="vague-container">
		<Vague width={window.innerWidth} height={window.innerHeight} on:render={handleVagueRender} />
	</div> -->

	<!-- <div class="bibi-container">
		<Bibi width={400} height={300} on:sceneInitialized={handleBibiSceneInitialized} />
	</div>  -->
</div>

<style>
	.scene-container {
		position: relative;
		width: 100%;
		height: 100vh;
	}
</style>
