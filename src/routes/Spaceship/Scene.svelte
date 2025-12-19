<script lang="ts">
	import Vaguend from '../vague/vaguend.svelte';
	import { T, useTask, useThrelte } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Spaceship from './models/spaceship.svelte';
	import {
		Color,
		Mesh,
		PMREMGenerator,
		PlaneGeometry,
		Raycaster,
		Vector2,
		Vector3,
		Group
	} from 'three';
	import { onMount, onDestroy } from 'svelte';
	import Stars from './Stars.svelte';
	import Nissan from './Nissan.svelte';
	import * as POST from 'postprocessing';

	const { scene, camera, renderer, renderStage, autoRender } = useThrelte();

	/** @type {import('three').Object3D} */
	let spaceShipRef = $state(new Group());
	let nissanRef = $state(new Group());
	let intersectionPoint = $state(new Vector3(0, 0, 0));
	let translY = $state(0);
	let translAccelleration = $state(0);
	let angleZ = $state(0);
	let angleAccelleration = $state(0);
	let rotationY = $state(0);

	let pmrem = new PMREMGenerator(renderer);
	let envMapRT: any;

	const composer = new POST.EffectComposer(renderer);
	const currentCamera = $derived((camera as any)?.current || camera);

	function setupEffectComposer(cam: THREE.Camera) {
		if (!cam || !scene) return;
		composer.removeAllPasses();
		composer.addPass(new POST.RenderPass(scene, cam));

		const bloomEffect = new POST.BloomEffect({
			intensity: 1.5,
			luminanceThreshold: 0.1,
			height: 1024
		});

		composer.addPass(new POST.EffectPass(cam, bloomEffect));
	}

	$effect(() => {
		if (currentCamera && currentCamera instanceof Color === false) {
			// tiny check to avoid weirdness
			setupEffectComposer(currentCamera);
		}
	});

	$effect(() => {
		const { width, height } = useThrelte().size.current;
		composer.setSize(width, height);
	});

	const setupEnvironmentMapping = () => {
		if (!renderer || !scene) return;
		if (envMapRT) envMapRT.dispose();

		envMapRT = pmrem.fromScene(scene, 0, 0.1, 1000);

		const updateMaterials = (object: any) => {
			if (!object) return;
			object.traverse((child: any) => {
				if (child.isMesh && child.material) {
					child.material.envMap = envMapRT.texture;
					child.material.envMapIntensity = 1.0;
					child.material.needsUpdate = true;
				}
			});
		};

		updateMaterials(spaceShipRef);
		updateMaterials(nissanRef);
	};

	useTask(
		(delta) => {
			// Simulation de vol
			const targetY = intersectionPoint.y;
			translAccelleration += (targetY - translY) * 0.002;
			translAccelleration *= 0.95;
			translY += translAccelleration;

			const dir = intersectionPoint.clone().sub(new Vector3(0, translY, 0)).normalize();
			const dirCos = dir.dot(new Vector3(0, 1, 0));
			const angle = Math.acos(dirCos) - Math.PI * 0.5;
			angleAccelleration += (angle - angleZ) * 0.01;
			angleAccelleration *= 0.85;
			angleZ += angleAccelleration;

			rotationY += 0.005;

			if (composer && currentCamera) {
				composer.render(delta);
			}
		},
		{ stage: renderStage, autoInvalidate: false }
	);

	onMount(() => {
		autoRender.set(false);

		const timeout = setTimeout(() => {
			setupEnvironmentMapping();
		}, 1000);

		const interval = setInterval(() => {
			setupEnvironmentMapping();
		}, 5000);

		return () => {
			autoRender.set(true);
			clearTimeout(timeout);
			clearInterval(interval);
			if (envMapRT) envMapRT.dispose();
			if (pmrem) pmrem.dispose();
		};
	});
</script>

<div class="div">
	<T.PerspectiveCamera makeDefault position={[-15, 10, 25]} fov={30}>
		<OrbitControls enableDamping target={[0, 0, 0]} />
	</T.PerspectiveCamera>

	<T.DirectionalLight intensity={3} position={[5, 15, 5]} castShadow />
	<T.AmbientLight intensity={0.5} />

	<Spaceship
		bind:ref={spaceShipRef}
		position={[0, translY, 0]}
		rotation={[angleZ, 0, angleZ, 'ZXY']}
	/>

	<Vaguend position={[0, -2, 0]} scale={20} />

	<Stars />

	<Nissan
		bind:ref={nissanRef}
		position={[2, translY + 0.5, -2]}
		rotation={[angleZ, rotationY, angleZ, 'ZXY']}
		scale={0.5}
	/>
</div>

<style>
	.div {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
	}
</style>
