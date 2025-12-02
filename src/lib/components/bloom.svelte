<script lang="ts">
	import {
		BloomEffect,
		EffectComposer,
		EffectPass,
		KernelSize,
		RenderPass,
		SMAAEffect,
		SMAAPreset,
	} from 'postprocessing'
	import { useThrelte, useTask } from '@threlte/core'
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	const { height = 512, width = 512, mipmapBlur = true } = $props();

	let composer: EffectComposer | undefined;

	// useThrelte and useTask must be called at the top level
	const { scene, renderer, camera } = useThrelte();

	onMount(() => {
		if (browser) {
			composer = new EffectComposer(renderer);
		}
	});

	$effect(() => {
		if (browser && composer && camera) {
			composer.removeAllPasses();
			composer.addPass(new RenderPass(scene, camera));
			composer.addPass(
				new EffectPass(
					camera,
					new BloomEffect({
						intensity: 0.8,
						luminanceThreshold: 0,
						height,
						width,
						luminanceSmoothing: 0,
						mipmapBlur,
						kernelSize: KernelSize.MEDIUM,
					})
				)
			);
			composer.addPass(
				new EffectPass(
					camera,
					new SMAAEffect({
						preset: SMAAPreset.LOW,
					})
				)
			);
		}
	});

	useTask(({ delta }) => {
		if (browser && composer) {
			composer.render(delta);
		}
	});
</script>