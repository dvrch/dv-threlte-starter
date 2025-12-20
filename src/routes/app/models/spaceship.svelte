<script lang="ts">
	import { AddEquation, CustomBlending, Group, LessEqualDepth, OneFactor } from 'three';
	import { T } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { createDracoLoader } from '$lib/utils/draco-loader';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfUrl = $state('');
	let mapUrl = $state('');

	const gltf = useGltf(() => gltfUrl || '', { dracoLoader: createDracoLoader() });
	const map = useTexture(() => mapUrl || '');

	onMount(async () => {
		if (browser) {
			gltfUrl = await getWorkingAssetUrl('spaceship.glb', 'models');
			mapUrl = await getWorkingAssetUrl('energy-beam-opacity.png', 'textures');
		}
	});

	let initialized = $state(false);
	$effect(() => {
		if ($gltf && !initialized) {
			const model = $gltf;
			function alphaFix(material: any) {
				if (!material) return;
				material.transparent = true;
				material.alphaToCoverage = true;
				material.depthFunc = LessEqualDepth;
				material.depthTest = true;
				material.depthWrite = true;
			}
			if (model.materials.spaceship_racer) alphaFix(model.materials.spaceship_racer);
			if (model.materials.cockpit) alphaFix(model.materials.cockpit);
			initialized = true;
		}
	});
</script>

<T is={ref} dispose={false} {...restProps}>
	{#if $gltf}
		<T.Group scale={0.003} rotation={[0, -Math.PI * 0.5, 0]} position={[0.95, 0, -2.235]}>
			{#if $gltf.nodes.Cube001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube001_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[739.26, -64.81, 64.77]}
				/>
			{/if}
			{#if $gltf.nodes.Cylinder002_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cylinder002_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[739.69, -59.39, -553.38]}
					rotation={[Math.PI / 2, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Cylinder003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cylinder003_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[742.15, -64.53, -508.88]}
					rotation={[Math.PI / 2, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Cube003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube003_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[737.62, 46.84, -176.41]}
				/>
			{/if}
			{#if $gltf.nodes.Cylinder004_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cylinder004_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[789.52, 59.45, -224.91]}
					rotation={[1, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Cube001_RExtr001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube001_RExtr001_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[745.54, 159.32, -5.92]}
				/>
			{/if}
			{#if $gltf.nodes.Cube001_RPanel003_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube001_RPanel003_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Cube001_RPanel003_RExtr_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube001_RPanel003_RExtr_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Cube002_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube002_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[736.79, -267.14, -33.21]}
				/>
			{/if}
			{#if $gltf.nodes.Cube001_RPanel001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube001_RPanel001_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Cube001_RPanel003_RExtr001_spaceship_racer_0}
				<T.Mesh
					castShadow
					receiveShadow
					geometry={$gltf.nodes.Cube001_RPanel003_RExtr001_spaceship_racer_0.geometry}
					material={$gltf.materials.spaceship_racer}
					position={[739.26, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Cube005_cockpit_0}
				<T.Mesh
					geometry={$gltf.nodes.Cube005_cockpit_0.geometry}
					material={$gltf.materials.cockpit}
					position={[739.45, 110.44, 307.18]}
					rotation={[0.09, 0, 0]}
				/>
			{/if}
			{#if $gltf.nodes.Sphere_cockpit_0}
				<T.Mesh
					geometry={$gltf.nodes.Sphere_cockpit_0.geometry}
					material={$gltf.materials.cockpit}
					position={[739.37, 145.69, 315.6]}
					rotation={[0.17, 0, 0]}
				/>
			{/if}

			{#if $map}
				<T.Mesh position={[740, -60, -1350]} rotation.x={Math.PI * 0.5}>
					<T.CylinderGeometry args={[70, 25, 1600, 15]} />
					<T.MeshBasicMaterial
						color="#ff6605"
						alphaMap={$map}
						transparent
						blending={CustomBlending}
						blendDst={OneFactor}
						blendEquation={AddEquation}
					/>
				</T.Mesh>
			{/if}
		</T.Group>
	{/if}

	<slot {ref} />
</T>
