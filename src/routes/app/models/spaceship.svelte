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
	import Stars from '../../Spaceship/Stars.svelte';

	let { ref = $bindable(new Group()), geometry, ...restProps } = $props();
	const { camera } = useThrelte();

	let gltfResultData = $state<any>(null);
	let mapResultData = $state<any>(null);
	let isLoading = $state(true);

	// --- Flight Simulation State (matching src/routes/Spaceship/Scene.svelte) ---
	let intersectionPoint = new Vector3(0, 0, 0);
	let translY = $state(0);
	let translAccelleration = $state(0);
	let angleZ = $state(0);
	let angleAccelleration = $state(0);
	let rotationRoll = $state(0);
	let rotationPitch = $state(0);

	const raycaster = new Raycaster();
	const pointer = new Vector2();
	const planeMesh = new Mesh(new PlaneGeometry(100, 100)); // Invisible plane for raycasting
	planeMesh.rotation.y = Math.PI * 0.5; // Rotate to face the default side camera better if needed, but in the original it's flat

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
				// Contrain X like in the original Spaceship scene
				intersectionPoint.x = 3;
			}
		}
	};

	useTask((delta) => {
		const mouseRadius = pointer.length();
		const activationRadius = 0.7; // Only react if mouse is within this radius
		const isActive = mouseRadius < activationRadius;

		// Translation follow mouse (Y axis) - Even slower as requested
		const targetY = isActive ? intersectionPoint.y : 0;
		translAccelleration += (targetY - translY) * 0.0007; // Extra dampened
		translAccelleration *= 0.94;
		translY += translAccelleration;

		// Fictive bounding box for vertical movement
		const boxLimit = 8;
		if (translY > boxLimit) {
			translY = boxLimit;
			translAccelleration = 0;
		}
		if (translY < -boxLimit) {
			translY = -boxLimit;
			translAccelleration = 0;
		}

		// Rotation follow (Z axis bank / angleZ)
		const dir = intersectionPoint.clone().sub(new Vector3(0, translY, 0)).normalize();
		const dirCos = dir.dot(new Vector3(0, 1, 0));
		const angle = Math.acos(dirCos) - Math.PI * 0.5;

		// Reaction only if active, otherwise return to neutral
		const targetAngle = isActive ? angle : 0;
		angleAccelleration += (targetAngle - angleZ) * 0.008;
		angleAccelleration *= 0.82;
		angleZ += angleAccelleration;

		// Pitch effect: Airplane style (Nose UP when ascending)
		// Reduced intensity for both kinetic and mouse pitch
		const kineticPitch = translAccelleration * 3.5;

		// Additional magnificent rotations (roll/tilt based on pointer lateral movement)
		const targetRoll = isActive ? -pointer.x * 0.6 : 0;
		const targetPitch = (isActive ? pointer.y * 0.12 : 0) + kineticPitch;

		// Interpolate for smoothness
		rotationRoll += (targetRoll - rotationRoll) * 0.04;
		rotationPitch += (targetPitch - rotationPitch) * 0.04;
	});

	onMount(() => {
		if (browser) {
			window.addEventListener('pointermove', handlePointerMove);
			loadAssets();
		}
	});

	onDestroy(() => {
		if (browser) {
			window.removeEventListener('pointermove', handlePointerMove);
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
			const processed = { ...rawGltf, nodes, materials };

			// Apply alpha fix and reflection settings
			function materialFix(material: any) {
				if (!material) return;
				material.transparent = true;
				material.alphaToCoverage = true;
				material.depthFunc = LessEqualDepth;
				material.depthTest = true;
				material.depthWrite = true;

				// Enable very strong reflections from Environment
				material.envMapIntensity = 60;
				if (material.normalScale) material.normalScale.set(0.3, 0.3);
			}

			Object.values(materials).forEach(materialFix);

			gltfResultData = processed;

			const texLoader = new TextureLoader();
			mapResultData = await texLoader.loadAsync(mapUrl);
		} catch (e) {
			console.error('Failed to load spaceship in app route:', e);
		} finally {
			isLoading = false;
		}
	}
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltfResultData}
		<!-- We apply the physics-based position and rotation (angleZ) -->
		<!-- This matches the logic from src/routes/Spaceship/Scene.svelte -->
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
