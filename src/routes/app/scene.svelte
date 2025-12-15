<script lang="ts">
	import Bibanime from './../bibi/bibanime.svelte';
	import Nissan from './models/Nissan.svelte';
	import { T } from '@threlte/core';
	import { Grid, OrbitControls, TransformControls } from '@threlte/extras';
	import * as Three from 'three';
	const { DEG2RAD } = Three.MathUtils;
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	// import Vague from '../vague/vague.svelte';
	// import Bibi from '../bibi/+page.svelte';

	// Créer une courbe fermée
	const curve = new Three.CatmullRomCurve3(
		[
			new Three.Vector3(-5, 0, 5),
			new Three.Vector3(0, 0, 5),
			new Three.Vector3(5, 0, 5),
			new Three.Vector3(5, 0, 0),
			new Three.Vector3(5, 0, -5),
			new Three.Vector3(0, 0, -5),
			new Three.Vector3(-5, 0, -5),
			new Three.Vector3(-5, 0, 0)
		],
		true
	);

	let curvePosition = Math.random();
	const speed = 0.005;

	let vagueMesh: Three.Mesh;
	let bibiScene: Three.Scene;
	let bibiCamera: Three.Camera;
	let bibiRenderer: Three.WebGLRenderer;

	let nissanPosition = $derived(curve.getPoint(curvePosition));
	let nissanRotation = $derived(
		new Three.Euler().setFromQuaternion(
			new Three.Quaternion().setFromUnitVectors(
				new Three.Vector3(0, 0, 1),
				curve.getTangent(curvePosition)
			)
		)
	);

	let bibanimePosition = $derived(curve.getPoint(curvePosition));
	let bibanimeRotation = $derived(
		new Three.Euler().setFromQuaternion(
			new Three.Quaternion().setFromUnitVectors(
				new Three.Vector3(0, 0, 1),
				curve.getTangent(curvePosition)
			)
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

<!-- Grid -->
<Grid cellColor="gray" sectionSize={0} />

<!-- Nissan -->
<Nissan position={[...nissanPosition]} rotation={[...nissanRotation]} let:ref castShadow>
	<TransformControls object={ref} />
</Nissan>

<Bibanime
	position={[bibanimePosition.x, bibanimePosition.y, bibanimePosition.z]}
	rotation={[bibanimeRotation.x, bibanimeRotation.y, bibanimeRotation.z]}
/>

<T.PerspectiveCamera
	makeDefault
	position={[-10, 10, 10]}
	fov={70}
	aspect={browser ? ((window.innerWidth * 0.3) / window.innerHeight) * 0.3 : 1}
>
	<OrbitControls
		autoRotate
		enableZoom={true}
		minDistance={0}
		maxDistance={80}
		target={[0, 1.5, 0]}
	/>
</T.PerspectiveCamera>

<!-- Curve visualization -->

<T.Points position.y={0.5}>
	<T.BufferGeometry>
		{#if curve}
			<T.Float32BufferAttribute
				attach="attributes-position"
				args={[curve.getPoints(50).flatMap((v) => [v.x, v.y, v.z]), 3]}
			/>
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
<style>
	.scene-container {
		position: relative;
		width: 100%;
		height: 100vh;
	}
</style>
