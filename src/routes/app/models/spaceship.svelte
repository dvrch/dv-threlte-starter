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
	import { onMount, onDestroy, untrack } from 'svelte';
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

	let keys = $state({
		ArrowLeft: false,
		ArrowRight: false
	});

	const raycaster = new Raycaster();
	const pointer = new Vector2();
	// Plane moved further back and made bigger to catch all rays
	const planeMesh = new Mesh(new PlaneGeometry(2000, 2000));
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
				intersectionPoint.x = 0;
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

		// Keyboard Override for vertical movement: Left/Right keys as requested
		let targetY = isActive ? intersectionPoint.y : 0;
		if (keys.ArrowLeft) targetY -= 20;
		if (keys.ArrowRight) targetY += 20;

		translAccelleration += (targetY - translY) * 0.002;
		translAccelleration *= 0.94;
		translY += translAccelleration;

		// Limit movement
		const boxLimit = 50;
		if (translY > boxLimit) {
			translY = boxLimit;
			translAccelleration = 0;
		}
		if (translY < -boxLimit) {
			translY = -boxLimit;
			translAccelleration = 0;
		}

		// Simplified Rotation logic for better predictability
		const targetAngle =
			isActive || keys.ArrowLeft || keys.ArrowRight ? (targetY - translY) * 0.05 : 0;
		angleAccelleration += (targetAngle - angleZ) * 0.05;
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

	// Handle Material Reflections reactively
	$effect(() => {
		if (gltfResultData && scene.environment) {
			console.log('✨ Applying environment map to spaceship materials');
			untrack(() => {
				gltfResultData.scene.traverse((child: any) => {
					if (child.isMesh && child.material) {
						child.material.envMap = scene.environment;
						child.material.envMapIntensity = 50;
						child.material.needsUpdate = true;
					}
				});
			});
		}
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
			console.log('🚀 Loading Spaceship GLB...');
			const gltfUrl = await getWorkingAssetUrl('spaceship.glb', 'models');
			const mapUrl = await getWorkingAssetUrl('energy-beam-opacity.png', 'textures');

			const loader = new GLTFLoader();
			loader.setDRACOLoader(createDracoLoader());

			const rawGltf = await loader.loadAsync(gltfUrl);
			console.log('✅ Spaceship GLB loaded successfully');

			const { nodes, materials } = buildSceneGraph(rawGltf);

			function materialFix(material: any) {
				if (!material) return;
				material.transparent = true;
				material.alphaToCoverage = true;
				material.depthFunc = LessEqualDepth;
				material.depthTest = true;
				material.depthWrite = true;

				// Premium reflections setup
				material.envMapIntensity = 50;
				if ('roughness' in material) material.roughness = 0.1;
				if ('metalness' in material) material.metalness = 1.0;
				if (material.normalScale) material.normalScale.set(0.2, 0.2);

				material.needsUpdate = true;
			}

			// Apply to all materials in the scene graph
			rawGltf.scene.traverse((child: any) => {
				if (child.isMesh) {
					materialFix(child.material);
				}
			});

			gltfResultData = rawGltf;

			const texLoader = new TextureLoader();
			mapResultData = await texLoader.loadAsync(mapUrl);
		} catch (e) {
			console.error('❌ Failed to load spaceship:', e);
		} finally {
			isLoading = false;
		}
	}
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltfResultData}
		<!-- We wrap everything in a group to apply flight physics and center it -->
		<T.Group
			position={[0, translY, 0]}
			rotation={[angleZ + rotationPitch, -Math.PI * 0.5, angleZ + rotationRoll]}
		>
			<!-- We render the whole scene to ensure all parts are visible -->
			<!-- Using a larger scale and position reset for visibility test -->
			<T is={gltfResultData.scene} scale={0.5} position={[0, 0, 0]} />

			<!-- Energy beam -->
			{#if mapResultData}
				<T.Mesh position={[0, 0, -13.5]} rotation.x={Math.PI * 0.5}>
					<T.CylinderGeometry args={[0.7, 0.25, 16, 15]} />
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
</T>
