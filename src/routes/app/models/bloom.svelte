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
	import * as THREE from 'three'; // Ajout de l'importation de THREE

	const {
		intensity = 0.8,
		luminanceThreshold = 0,
		height = 512,
		width = 512,
		luminanceSmoothing = 0,
		mipmapBlur = true
	} = $props();

	const { scene, renderer, camera, autoRender } = useThrelte();
	const composer = new EffectComposer(renderer);

	const setupEffectComposer = (cam: THREE.Camera) => {
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
	};

	$effect(() => {
		if (camera.current) {
			setupEffectComposer(camera.current);
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
			if (!composer || !camera.current || !scene) return;
			composer.render(delta);
		},
		{ stage: 'after' }
	);
</script>
