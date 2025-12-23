<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { Group, AnimationMixer } from 'three';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	let { ref = $bindable(new Group()), children, ...rest } = $props();

	let gltfData = $state<any>(null);
	let mixer = $state<AnimationMixer | null>(null);

	onMount(async () => {
		if (browser) {
			try {
				const url = await getWorkingAssetUrl('bibi3.glb', 'models');
				console.log('🤖 Loading Bibi Game GLB from:', url);
				const loader = new GLTFLoader();
				loader.setDRACOLoader(createDracoLoader());

				const rawGltf = await loader.loadAsync(url);
				console.log('✅ Bibi Game GLB loaded:', rawGltf);
				buildSceneGraph(rawGltf);
				gltfData = rawGltf;

				// Setup animations
				if (rawGltf.animations && rawGltf.animations.length > 0) {
					mixer = new AnimationMixer(rawGltf.scene);
					rawGltf.animations.forEach((clip: any) => {
						const action = mixer!.clipAction(clip);
						action.play();
					});
					console.log(`🎬 Playing ${rawGltf.animations.length} Bibi animations`);
				}

				window.dispatchEvent(new Event('modelVisualLoaded'));
			} catch (e) {
				console.error('Failed to load Bibi model:', e);
			}
		}
	});

	// Update animation mixer
	useTask((delta) => {
		if (mixer) {
			mixer.update(delta);
		}
	});
</script>

<T is={ref} dispose={false} {...rest}>
	{#if gltfData}
		<T.Group scale={1}>
			<T is={gltfData.scene} />
		</T.Group>
	{/if}

	{@render children?.({ ref })}
</T>
