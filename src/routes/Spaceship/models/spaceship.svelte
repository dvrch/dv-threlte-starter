<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { Group, LessEqualDepth } from 'three';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { createDracoLoader } from '$lib/utils/draco-loader';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfUrl = $state('');
	let mapUrl = $state('');

	// Reactive loaders for Threlte 8
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
		<T.Group scale={0.01}>
			<T is={$gltf.scene} />
		</T.Group>

		{#if $map}
			<T.Mesh position={[0, -0.6, -13.5]} rotation.x={Math.PI * 0.5} scale={100}>
				<T.CylinderGeometry args={[0.7, 0.25, 16, 15]} />
				<T.MeshBasicMaterial color="#ff6605" alphaMap={$map} transparent />
			</T.Mesh>
		{/if}
	{:else}
		<slot name="fallback" />
	{/if}

	<slot {ref} />
</T>
