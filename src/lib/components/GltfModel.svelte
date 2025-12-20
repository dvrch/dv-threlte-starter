<script lang="ts">
	import { T } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';
	import { AnimationMixer } from 'three';

	// Receive URL and other props
	let { url, ...restProps }: { url: string; [key: string]: any } = $props();

	let gltfResult = $state<any>(null);
	let isLoading = $state(true);
	let mixer: AnimationMixer | null = null;

	onMount(async () => {
		if (browser && url) {
			try {
				const filename = url.split('/').pop() || url;
				const resolved = await getWorkingAssetUrl(filename, 'models');

				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const result = await loader.loadAsync(resolved);
				gltfResult = result;

				if (result.animations && result.animations.length > 0) {
					mixer = new AnimationMixer(result.scene);
					result.animations.forEach((clip: any) => {
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

	// Task for animation updates
	import { useTask } from '@threlte/core';
	useTask((delta) => {
		if (mixer) mixer.update(delta);
	});
</script>

{#if browser && gltfResult}
	<T is={gltfResult.scene} {...restProps} />
{:else}
	<T.Group />
{/if}
