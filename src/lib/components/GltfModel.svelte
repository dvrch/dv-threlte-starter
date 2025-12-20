<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';
	import { AnimationMixer } from 'three';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	// Receive URL and other props
	let { url, ...restProps }: { url: string; [key: string]: any } = $props();

	let gltfScene = $state<any>(null);
	let isLoading = $state(true);
	let mixer: AnimationMixer | null = null;

	onMount(async () => {
		if (browser && url) {
			try {
				const filename = url.split('/').pop() || url;
				const resolved = await getWorkingAssetUrl(filename, 'models');

				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const raw = await loader.loadAsync(resolved);
				const { nodes, materials } = buildSceneGraph(raw);
				gltfScene = { ...raw, nodes, materials };

				if (raw.animations && raw.animations.length > 0) {
					mixer = new AnimationMixer(raw.scene);
					raw.animations.forEach((clip: any) => {
						mixer?.clipAction(clip).play();
					});
				}
			} catch (e) {
				console.error(`Failed to load GLTF from ${url}:`, e);
			} finally {
				isLoading = false;
			}
		}
	});

	useTask((delta) => {
		if (mixer) mixer.update(delta);
	});
</script>

{#if browser && gltfScene}
	<T is={gltfScene.scene} {...restProps} />
{:else}
	<T.Group />
{/if}
