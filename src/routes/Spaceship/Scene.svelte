<script>
	import Vague from '../vague/+page.svelte';
	import { T, useTask, useThrelte } from '@threlte/core';
	import { OrbitControls, useGltf } from '@threlte/extras';
	import Spaceship from './models/spaceship.svelte';
	import { Color, Mesh, PMREMGenerator, PlaneGeometry, Raycaster, Vector2, Vector3 } from 'three';
	import { onMount, onDestroy } from 'svelte';
	import Stars from './Stars.svelte';
	import Nissan from './Nissan.svelte';
	import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
	import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
	import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
	import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';

	const { scene, camera, renderer } = useThrelte();

	/** @type {import('three').Object3D} */
	let spaceShipRef = $state(null);
	let intersectionPoint = $state(null);
	let translY = $state(0);
	let translAccelleration = $state(0);
	let angleZ = $state(0);
	let angleAccelleration = $state(0);
	let pmrem = new PMREMGenerator(renderer);
	let envMapRT;

	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';
	let ni = useGltf(getCloudinaryAssetUrl(`/assets/nissan.glb`));

	const composer = new EffectComposer(renderer);
	composer.setSize(innerWidth, innerHeight);

	const setupEffectComposer = () => {
		const renderPass = new RenderPass(scene, camera.current);
		composer.addPass(renderPass);

		const bloomPass = new UnrealBloomPass(new Vector2(innerWidth, innerHeight), 0.275, 1, 0);
		composer.addPass(bloomPass);

		const outputPass = new OutputPass();
		composer.addPass(outputPass);
	};

	let cleanupFunctions = [];

	const setupEnvironmentMapping = () => {
		if (envMapRT) envMapRT.dispose();

		scene.background = null;
		envMapRT = pmrem.fromScene(scene, 0, 0.1, 1000);

		const updateMaterials = (object) => {
			object.traverse((child) => {
				if (child?.material?.envMapIntensity) {
					child.material.envMap = envMapRT.texture;
					child.material.envMapIntensity = 100;
					child.material.normalScale?.set(0.3, 0.3);
					child.material.needsUpdate = true;
				}
			});
		};

		if (spaceShipRef) updateMaterials(spaceShipRef);
		const nissanRef = scene.getObjectByName('Nissan');
		if (nissanRef) updateMaterials(nissanRef);
	};

	useTask(({ scene, delta }) => {
		if (intersectionPoint) {
			const targetY = intersectionPoint?.y || 0;
			translAccelleration += (targetY - translY) * 0.002; // stiffness
			translAccelleration *= 0.95; // damping
			translY += translAccelleration;

			const dir = intersectionPoint.clone().sub(new Vector3(0, translY, 0)).normalize();
			const dirCos = dir.dot(new Vector3(0, 1, 0));
			const angle = Math.acos(dirCos) - Math.PI * 0.5;
			angleAccelleration += (angle - angleZ) * 0.01; // stiffness
			angleAccelleration *= 0.85; // damping
			angleZ += angleAccelleration;
		}

		setupEnvironmentMapping();
		composer.render();
	});

	onMount(() => {
		setupEffectComposer();

		setupEnvironmentMapping();

		const interval = setInterval(() => {
			setupEnvironmentMapping();
		}, 1000); // Rafraîchir l'environnement toutes les secondes

		cleanupFunctions.push(() => clearInterval(interval));
	});

	onDestroy(() => {
		cleanupFunctions.forEach((fn) => fn());
		if (envMapRT) envMapRT.dispose();
	});

	let canvas;
</script>

<div class="div">
	<T.PerspectiveCamera makeDefault position={[-5, 6, 10]} fov={25}>
		<OrbitControls enableDamping target={[0, 0, 0]} />
	</T.PerspectiveCamera>

	<T.DirectionalLight intensity={1.8} position={[0, 10, 0]} castShadow shadow.bias={-0.0001} />
	<!-- <T.AmbientLight intensity={0.5} /> -->

	<Spaceship
		bind:ref={spaceShipRef}
		position={[0, translY, 0]}
		rotation={[angleZ, 0, angleZ, 'ZXY']}
	/>

	<Vague bind:ref={spaceShipRef} position={[0, translY, 0]} scale={6} />

	<Stars />

	<Nissan
		bind:ref={spaceShipRef}
		position={[0, translY, 0]}
		rotation={[angleZ, 80, angleZ, 'ZXY']}
	/>
</div>

<style>
	.div {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -2;
	}
</style>
