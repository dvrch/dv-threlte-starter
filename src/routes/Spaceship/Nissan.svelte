<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { Group, LessEqualDepth } from 'three';
	import Bloom from './bloom.svelte';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfUrl = $state<string | null>(null);

	onMount(async () => {
		if (browser) {
			gltfUrl = await getWorkingAssetUrl('nissan2.glb', 'models');
		}
	});

	const gltf = $derived(gltfUrl ? useGltf(gltfUrl, { dracoLoader: createDracoLoader() }) : null);

	let initialized = $state(false);

	$effect(() => {
		if (gltf) {
			gltf.then((model: any) => {
				if (initialized) return;

				function alphaFix(material: any) {
					if (!material) return;
					material.transparent = true;
					material.alphaToCoverage = true;
					material.depthFunc = LessEqualDepth;
					material.depthTest = true;
					material.depthWrite = true;
				}

				model.scene.traverse((child: any) => {
					if (child.isMesh) {
						alphaFix(child.material);
					}
				});
				initialized = true;
			});
		}
	});
</script>

{#if browser}
	<Bloom />
{/if}

<T is={ref} dispose={false} {...restProps}>
	{#if gltf}
		{#await gltf then value}
			<T is={value.scene} />
		{/await}
	{:else}
		<slot name="fallback" />
	{/if}
</T>
