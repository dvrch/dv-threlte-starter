<script lang="ts">
	import {
		AddEquation,
		CustomBlending,
		Group,
		LessEqualDepth,
		OneFactor,
		TextureLoader
	} from 'three';
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { createDracoLoader } from '$lib/utils/draco-loader';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfResult = $state<any>(null);
	let mapResult = $state<any>(null);
	let isLoading = $state(true);

	onMount(async () => {
		if (browser) {
			try {
				const gltfUrl = await getWorkingAssetUrl('spaceship.glb', 'models');
				const mapUrl = await getWorkingAssetUrl('energy-beam-opacity.png', 'textures');

				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const rawGltf = await loader.loadAsync(gltfUrl);

				// Apply alpha fix
				function alphaFix(material: any) {
					if (!material) return;
					material.transparent = true;
					material.alphaToCoverage = true;
					material.depthFunc = LessEqualDepth;
					material.depthTest = true;
					material.depthWrite = true;
				}
				if (rawGltf.materials.spaceship_racer) alphaFix(rawGltf.materials.spaceship_racer);
				if (rawGltf.materials.cockpit) alphaFix(rawGltf.materials.cockpit);

				gltfResult = rawGltf;

				const texLoader = new TextureLoader();
				mapResult = await texLoader.loadAsync(mapUrl);
			} catch (e) {
				console.error('Failed to load spaceship in app route:', e);
			} finally {
				isLoading = false;
			}
		}
	});
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if gltfResult}
		<T.Group scale={0.003} rotation={[0, -Math.PI * 0.5, 0]} position={[0.95, 0, -2.235]}>
			{#if gltfResult.nodes.Cube001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube001_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[739.26, -64.81, 64.77]}
				/>
			{/if}
			{#if gltfResult.nodes.Cylinder002_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cylinder002_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[739.69, -59.39, -553.38]}
					rotation={[Math.PI / 2, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Cylinder003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cylinder003_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[742.15, -64.53, -508.88]}
					rotation={[Math.PI / 2, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube003_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[737.62, 46.84, -176.41]}
				/>
			{/if}
			{#if gltfResult.nodes.Cylinder004_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cylinder004_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[789.52, 59.45, -224.91]}
					rotation={[1, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube001_RExtr001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube001_RExtr001_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[745.54, 159.32, -5.92]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube001_RPanel003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube001_RPanel003_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube001_RPanel003_RExtr_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube001_RPanel003_RExtr_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube002_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube002_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[736.79, -267.14, -33.21]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube001_RPanel001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube001_RPanel001_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube001_RPanel003_RExtr001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={gltfResult.nodes.Cube001_RPanel003_RExtr001_spaceship_racer_0.geometry}
					material={gltfResult.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Cube005_cockpit_0}
				<T.Mesh
					geometry={gltfResult.nodes.Cube005_cockpit_0.geometry}
					material={gltfResult.materials.cockpit}
					position={[739.45, 110.44, 307.18]}
					rotation={[0.09, 0, 0]}
				/>
			{/if}
			{#if gltfResult.nodes.Sphere_cockpit_0}
				<T.Mesh
					geometry={gltfResult.nodes.Sphere_cockpit_0.geometry}
					material={gltfResult.materials.cockpit}
					position={[739.37, 145.69, 315.6]}
					rotation={[0.17, 0, 0]}
				/>
			{/if}

			{#if mapResult}
				<T.Mesh position={[740, -60, -1350]} rotation.x={Math.PI * 0.5}>
					<T.CylinderGeometry args={[70, 25, 1600, 15]} />
					<T.MeshBasicMaterial
						color="#ff6605"
						alphaMap={mapResult}
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
