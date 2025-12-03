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
	import * as THREE from 'three'; // Ajout de l'importation de THREE

	const { intensity = 0.8, luminanceThreshold = 0, height = 512, width = 512, luminanceSmoothing = 0, mipmapBlur = true } = $props();

	const { scene, renderer, camera } = useThrelte()
	const composer = new EffectComposer(renderer)

	const setupEffectComposer = (camera: THREE.Camera) => {
		composer.removeAllPasses()
		composer.addPass(new RenderPass(scene, camera))
		composer.addPass(
			new EffectPass(
				camera,
				new BloomEffect({
					intensity,
					luminanceThreshold,
					height,
					width,
					luminanceSmoothing,
					mipmapBlur,
					kernelSize: KernelSize.MEDIUM,
				})
			)
		)
		composer.addPass(
			new EffectPass(
				camera,
				new SMAAEffect({
					preset: SMAAPreset.LOW,
				})
			)
		)
	}

	$effect(() => { if ($camera) { setupEffectComposer($camera); } })

	useTask(({ delta }) => {
		if (!composer || !$camera || !$scene) return;
		composer.render(delta)
	})
</script>
