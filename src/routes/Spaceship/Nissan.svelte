<script lang="ts">
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { Group, LessEqualDepth } from 'three';
	import Bloom from './bloom.svelte';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';

	let { ref = $bindable(new Group()), ...restProps } = $props();

	let gltfResult = $state<any>(null);
	let isLoading = $state(true);

	onMount(async () => {
		if (browser) {
			try {
				const url = await getWorkingAssetUrl('nissan2.glb', 'models');
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const model = await loader.loadAsync(url);

				// Apply alpha fix
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

				gltfResult = model;
			} catch (e) {
				console.error('Failed to load Nissan in spaceship route:', e);
			} finally {
				isLoading = false;
			}
		}
	});
</script>

{#if browser}
	<Bloom />
{/if}

<T is={ref} dispose={false} {...restProps}>
	{#if gltfResult}
		<T is={gltfResult.scene} />
	{:else if isLoading}
		<slot name="fallback" />
	{/if}
</T>
