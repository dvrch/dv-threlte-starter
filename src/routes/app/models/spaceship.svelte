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
		PlaneGeometry,
		PMREMGenerator
	} from 'three';
	import { T, useTask, useThrelte } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount, onDestroy, untrack } from 'svelte';
	import { browser } from '$app/environment';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let { ref = $bindable(new Group()), geometry, ...restProps } = $props();
	const { camera, scene, renderer } = useThrelte();

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
	const planeMesh = new Mesh(new PlaneGeometry(2000, 2000));
	planeMesh.rotation.y = Math.PI * 0.5;

	// Dynamic Env Map (Capturing stars & scene glow)
	let pmrem = new PMREMGenerator(renderer);
	let dynamicEnvMap: any = null;

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

		let targetY = isActive ? intersectionPoint.y : 0;
		if (keys.ArrowLeft) targetY -= 20;
		if (keys.ArrowRight) targetY += 20;

		translAccelleration += (targetY - translY) * 0.002;
		translAccelleration *= 0.94;
		translY += translAccelleration;

		const boxLimit = 50;
		if (translY > boxLimit) {
			translY = boxLimit;
			translAccelleration = 0;
		}
		if (translY < -boxLimit) {
			translY = -boxLimit;
			translAccelleration = 0;
		}

		const targetAngle =
			isActive || keys.ArrowLeft || keys.ArrowRight ? (targetY - translY) * 0.05 : 0;
		angleAccelleration += (targetAngle - angleZ) * 0.05;
		angleAccelleration *= 0.82;
		angleZ += angleAccelleration;

		const kineticPitch = translAccelleration * 3.5;
		const kineticRoll = translAccelleration * 5.0;

		const targetRoll = (isActive ? -pointer.x * 0.5 : 0) + kineticRoll;
		const targetPitch = (isActive ? pointer.y * 0.1 : 0) + kineticPitch;

		rotationRoll += (targetRoll - rotationRoll) * 0.04;
		rotationPitch += (targetPitch - rotationPitch) * 0.04;
	});

	// Robust material update function
	function materialFix(material: any, envTexture: any = null) {
		if (!material) return;
		material.transparent = true;
		material.alphaToCoverage = true;
		material.depthFunc = LessEqualDepth;
		material.depthTest = true;
		material.depthWrite = true;

		// Extreme reflections logic from /Spaceship
		material.envMapIntensity = 100; // Max intensity
		if ('roughness' in material) material.roughness = 0.02; // Super shiny
		if ('metalness' in material) material.metalness = 1.0;
		if (material.normalScale) material.normalScale.set(0.1, 0.1); // Smoother

		if (envTexture) {
			material.envMap = envTexture;
		} else if (scene.environment) {
			material.envMap = scene.environment;
		}

		// Emissive boost
		if ('emissive' in material && material.emissive) {
			material.emissiveIntensity = 15; // Make the lights shine!
		}

		material.needsUpdate = true;
	}

	function updateAllMaterials(envTexture: any = null) {
		if (!gltfResultData) return;
		gltfResultData.scene.traverse((child: any) => {
			if (child.isMesh && child.material) {
				materialFix(child.material, envTexture);
			}
		});
	}

	// Dynamic Env Map capturing stars
	const captureEnvMap = () => {
		if (!renderer || !scene) return;
		if (dynamicEnvMap) dynamicEnvMap.dispose();
		dynamicEnvMap = pmrem.fromScene(scene, 0, 0.1, 1000);
		updateAllMaterials(dynamicEnvMap.texture);
	};

	$effect(() => {
		if (gltfResultData) {
			updateAllMaterials();
		}
	});

	onMount(() => {
		if (browser) {
			window.addEventListener('pointermove', handlePointerMove);
			window.addEventListener('keydown', handleKeyDown);
			window.addEventListener('keyup', handleKeyUp);
			loadAssets();

			// Periodic env map capture to catch stars
			const interval = setInterval(captureEnvMap, 3000);
			return () => clearInterval(interval);
		}
	});

	onDestroy(() => {
		if (browser) {
			window.removeEventListener('pointermove', handlePointerMove);
			window.removeEventListener('keydown', handleKeyDown);
			window.removeEventListener('keyup', handleKeyUp);
			if (dynamicEnvMap) dynamicEnvMap.dispose();
			pmrem.dispose();
		}
	});

	async function loadAssets() {
		try {
			const gltfUrl = await getWorkingAssetUrl('spaceship.glb', 'models');
			const mapUrl = await getWorkingAssetUrl('energy-beam-opacity.png', 'textures');

			const loader = new GLTFLoader();
			loader.setDRACOLoader(createDracoLoader());

			const rawGltf = await loader.loadAsync(gltfUrl);
			buildSceneGraph(rawGltf); // ensure internal nodes/materials are ready if needed
			gltfResultData = rawGltf;

			updateAllMaterials();

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
		<T.Group
			position={[0, translY, 0]}
			rotation={[angleZ + rotationPitch, -Math.PI * 0.5, angleZ + rotationRoll]}
		>
			<T is={gltfResultData.scene} scale={0.5} position={[0, 0, 0]} />

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
