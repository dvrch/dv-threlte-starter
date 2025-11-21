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
	import { useThrelte, useFrame } from '@threlte/core'
	import * as THREE from 'three'; // Ajout de l'importation de THREE

	export let intensity = 0.8;
	export let luminanceThreshold = 0;
	export let height = 512;
	export let width = 512;
	export let luminanceSmoothing = 0;
	export let mipmapBlur = true;

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

	$: setupEffectComposer($camera)

	useFrame((_, delta) => {
		composer.render(delta)
	})
</script>
