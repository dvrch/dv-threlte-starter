<script lang="ts">
	import {
		AddEquation,
		CustomBlending,
		Group,
		LessEqualDepth,
		OneFactor,
		TextureLoader,
		Vector2,
		Vector3
	} from 'three';
	import { T, useTask } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';
	import Stars from '../../Spaceship/Stars.svelte';

	let { ref = $bindable(new Group()), geometry, ...restProps } = $props();

	let gltfResultData = $state<any>(null);
	let mapResultData = $state<any>(null);
	let isLoading = $state(true);

	// Reactivity state
	let mouse = new Vector2(0, 0);
	let targetRotation = new Vector3(0, 0, 0);
	let currentRotation = $state(new Vector3(0, 0, 0));
	let currentPosition = $state(new Vector3(0, 0, 0));

	const handleMouseMove = (e: MouseEvent) => {
		mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
		mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
	};

	useTask((delta) => {
		// Smoothing the movement
		targetRotation.z = -mouse.x * 0.5; // Roll
		targetRotation.x = -mouse.y * 0.3; // Pitch

		currentRotation.x += (targetRotation.x - currentRotation.x) * 0.1;
		currentRotation.z += (targetRotation.z - currentRotation.z) * 0.1;

		currentPosition.y += (mouse.y * 2 - currentPosition.y) * 0.05;
		currentPosition.z += (-mouse.x * 2 - currentPosition.z) * 0.05;
	});

	onMount(() => {
		if (browser) {
			window.addEventListener('mousemove', handleMouseMove);
			loadAssets();
		}
	});

	onDestroy(() => {
		if (browser) {
			window.removeEventListener('mousemove', handleMouseMove);
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

			// Apply alpha fix
			function alphaFix(material: any) {
				if (!material) return;
				material.transparent = true;
				material.alphaToCoverage = true;
				material.depthFunc = LessEqualDepth;
				material.depthTest = true;
				material.depthWrite = true;
			}
			if (materials.spaceship_racer) alphaFix(materials.spaceship_racer);
			if (materials.cockpit) alphaFix(materials.cockpit);

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
	<T.Group rotation={[0, Math.PI * 0.5, 0]}>
		<Stars />
	</T.Group>

	{#if gltfResultData}
		<T.Group
			scale={0.001}
			rotation={[currentRotation.x, -Math.PI * 0.5, currentRotation.z]}
			position={[currentPosition.x, currentPosition.y, currentPosition.z]}
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
