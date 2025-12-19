<script lang="ts">
	import {
		BloomEffect,
		EffectComposer,
		EffectPass,
		KernelSize,
		RenderPass,
		SMAAEffect,
		SMAAPreset
	} from 'postprocessing';
	import { useThrelte, useTask } from '@threlte/core';
	import * as THREE from 'three';

	let {
		intensity = 0.8,
		luminanceThreshold = 0,
		height = 512,
		width = 512,
		luminanceSmoothing = 0,
		mipmapBlur = true
	} = $props();

	const { scene, renderer, camera, autoRender, renderStage } = useThrelte();
	const composer = new EffectComposer(renderer);

	// Threlte 8 + Svelte 5 handling: camera can be a store or a direct ref.
	// $derived handles reactivity automatically.
	const currentCamera = $derived((camera as any)?.current || camera);

	function setupEffectComposer(cam: THREE.Camera) {
		if (!cam || !scene) return;
		composer.removeAllPasses();
		composer.addPass(new RenderPass(scene, cam));
		composer.addPass(
			new EffectPass(
				cam,
				new BloomEffect({
					intensity,
					luminanceThreshold,
					height,
					width,
					luminanceSmoothing,
					mipmapBlur,
					kernelSize: KernelSize.MEDIUM
				})
			)
		);
		composer.addPass(
			new EffectPass(
				cam,
				new SMAAEffect({
					preset: SMAAPreset.LOW
				})
			)
		);
	}

	$effect(() => {
		// Track dependencies to recreate passes when props change
		intensity;
		luminanceThreshold;
		height;
		width;
		luminanceSmoothing;
		mipmapBlur;

		if (currentCamera && currentCamera instanceof THREE.Camera) {
			setupEffectComposer(currentCamera);
		}
	});

	$effect(() => {
		const initialAutoRender = autoRender.current;
		autoRender.set(false);
		return () => {
			autoRender.set(initialAutoRender);
		};
	});

	useTask(
		({ delta }) => {
			// Only render if we have a valid camera and passes
			if (!composer || !currentCamera || composer.passes.length < 2) return;
			composer.render(delta);
		},
		{ stage: renderStage }
	);
</script>
