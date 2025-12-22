<script lang="ts">
	import {
		AddEquation,
		CustomBlending,
		Group,
		LessEqualDepth,
		OneFactor,
		TextureLoader,
		Vector2,
		Vector3,
		Raycaster,
		Mesh,
		PlaneGeometry
	} from 'three';
	import { T, useTask, useThrelte } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let { ref = $bindable(new Group()), geometry, ...restProps } = $props();
	const { camera, scene } = useThrelte();

	let gltfResultData = $state<any>(null);
	let mapResultData = $state<any>(null);
	let isLoading = $state(true);

	// --- Flight Simulation State ---
	let intersectionPoint = new Vector3(0, 0, 0);
	let translY = $state(0);
	let translAccelleration = $state(0);
	let angleZ = $state(0);
	let angleAccelleration = $state(0);
	let rotationRoll = $state(0);
	let rotationPitch = $state(0);

	let keys = {
		ArrowLeft: false,
		ArrowRight: false
	};

	const raycaster = new Raycaster();
	const pointer = new Vector2();
	const planeMesh = new Mesh(new PlaneGeometry(500, 500));
	planeMesh.rotation.y = Math.PI * 0.5;

	const handlePointerMove = (event: PointerEvent) => {
		if (!browser) return;
		pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
		pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;

		const currentCamera = (camera as any)?.current || camera;
		if (currentCamera && currentCamera.isCamera) {
			raycaster.setFromCamera(pointer, currentCamera);
			const intersects = raycaster.intersectObject(planeMesh);
			if (intersects[0]) {
				intersectionPoint.copy(intersects[0].point);
				intersectionPoint.x = 0; // Keep it centered in the global app view
			}
		}
	};

	const handleKeyDown = (e: KeyboardEvent) => {
		if (e.key in keys) keys[e.key as keyof typeof keys] = true;
	};
	const handleKeyUp = (e: KeyboardEvent) => {
		if (e.key in keys) keys[e.key as keyof typeof keys] = false;
	};

	useTask((delta) => {
		const mouseRadius = pointer.length();
		const activationRadius = 2.5;
		const isActive = mouseRadius < activationRadius;

		// Keyboard Override for vertical movement
		let targetY = isActive ? intersectionPoint.y : 0;
		if (keys.ArrowLeft) targetY -= 15;
		if (keys.ArrowRight) targetY += 15;

		translAccelleration += (targetY - translY) * 0.002;
		translAccelleration *= 0.94;
		translY += translAccelleration;

		// Limit movement
		const boxLimit = 30;
		if (translY > boxLimit) {
			translY = boxLimit;
			translAccelleration = 0;
		}
		if (translY < -boxLimit) {
			translY = -boxLimit;
			translAccelleration = 0;
		}

		// Rotation logic
		const dir = new Vector3(0, targetY, 0).sub(new Vector3(0, translY, 0)).normalize();
		const dirCos = dir.dot(new Vector3(0, 1, 0));
		const angle = isNaN(dirCos) ? 0 : Math.acos(dirCos) - Math.PI * 0.5;

		const targetAngle = isActive || keys.ArrowLeft || keys.ArrowRight ? angle : 0;
		angleAccelleration += (targetAngle - angleZ) * 0.01;
		angleAccelleration *= 0.82;
		angleZ += angleAccelleration;

		// Airplane kinetics
		const kineticPitch = translAccelleration * 3.5;
		const kineticRoll = translAccelleration * 5.0;

		const targetRoll = (isActive ? -pointer.x * 0.5 : 0) + kineticRoll;
		const targetPitch = (isActive ? pointer.y * 0.1 : 0) + kineticPitch;

		rotationRoll += (targetRoll - rotationRoll) * 0.04;
		rotationPitch += (targetPitch - rotationPitch) * 0.04;
	});

	onMount(() => {
		if (browser) {
			window.addEventListener('pointermove', handlePointerMove);
			window.addEventListener('keydown', handleKeyDown);
			window.addEventListener('keyup', handleKeyUp);
			loadAssets();
		}
	});

	onDestroy(() => {
		if (browser) {
			window.removeEventListener('pointermove', handlePointerMove);
			window.removeEventListener('keydown', handleKeyDown);
			window.removeEventListener('keyup', handleKeyUp);
		}
	});

	async function loadAssets() {
		try {
			const gltfUrl = await getWorkingAssetUrl('spaceship.glb', 'models');
			const mapUrl = await getWorkingAssetUrl('energy-beam-opacity.png', 'textures');

			const loader = new GLTFLoader();
			loader.setDRACOLoader(createDracoLoader());

			const rawGltf = await loader.loadAsync(gltfUrl);
			const { nodes, materials } = buildSceneGraph(rawGltf);

			function materialFix(material: any) {
				if (!material) return;
				material.transparent = true;
				material.alphaToCoverage = true;
				material.depthFunc = LessEqualDepth;
				material.depthTest = true;
				material.depthWrite = true;

				// Premium reflections like the original route
				material.envMapIntensity = 50;
				if ('roughness' in material) material.roughness = 0.1;
				if ('metalness' in material) material.metalness = 1.0;
				if (material.normalScale) material.normalScale.set(0.2, 0.2);

				material.needsUpdate = true;
			}

			Object.values(materials).forEach(materialFix);

			$effect(() => {
				if (scene.environment) {
					Object.values(materials).forEach((mat: any) => {
						if (mat) {
							mat.envMap = scene.environment;
							mat.needsUpdate = true;
						}
					});
				}
			});

			gltfResultData = { nodes, materials, scene: rawGltf.scene };
			const texLoader = new TextureLoader();
			mapResultData = await texLoader.loadAsync(mapUrl);
		} catch (e) {
			console.error('Failed to load spaceship:', e);
		} finally {
			isLoading = false;
		}
	}
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltfResultData}
		<T.Group
			scale={0.01}
			position={[0, translY, 0]}
			rotation={[angleZ + rotationPitch, -Math.PI * 0.5, angleZ + rotationRoll]}
		>
			{#if gltfResultData.nodes.Cube001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube001_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[739.26, -64.81, 64.77]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cylinder002_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cylinder002_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[739.69, -59.39, -553.38]}
					rotation={[Math.PI / 2, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cylinder003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cylinder003_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[742.15, -64.53, -508.88]}
					rotation={[Math.PI / 2, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube003_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[737.62, 46.84, -176.41]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cylinder004_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cylinder004_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[789.52, 59.45, -224.91]}
					rotation={[1, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube001_RExtr001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube001_RExtr001_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[745.54, 159.32, -5.92]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube001_RPanel003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube001_RPanel003_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube001_RPanel003_RExtr_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube001_RPanel003_RExtr_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube002_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube002_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[736.79, -267.14, -33.21]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube001_RPanel001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube001_RPanel001_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube001_RPanel003_RExtr001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResultData.nodes.Cube001_RPanel003_RExtr001_spaceship_racer_0.geometry}
					material={gltfResultData.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Cube005_cockpit_0}
				<T.Mesh
					geometry={gltfResultData.nodes.Cube005_cockpit_0.geometry}
					material={gltfResultData.materials.cockpit}
					position={[739.45, 110.44, 307.18]}
					rotation={[0.09, 0, 0]}
				/>
			{/if}
			{#if gltfResultData.nodes.Sphere_cockpit_0}
				<T.Mesh
					geometry={gltfResultData.nodes.Sphere_cockpit_0.geometry}
					material={gltfResultData.materials.cockpit}
					position={[739.37, 145.69, 315.6]}
					rotation={[0.17, 0, 0]}
				/>
			{/if}

			{#if mapResultData}
				<T.Mesh position={[740, -60, -1350]} rotation.x={Math.PI * 0.5}>
					<T.CylinderGeometry args={[70, 25, 1600, 15]} />
					<T.MeshBasicMaterial
						color="#ff6605"
						alphaMap={mapResultData}
						transparent
						blending={CustomBlending}
						blendDst={OneFactor}
						blendEquation={AddEquation}
					/>
				</T.Mesh>
			{/if}
		</T.Group>
	{:else if isLoading}
		<slot name="fallback" />
	{/if}

	<slot {ref} />
</T>
