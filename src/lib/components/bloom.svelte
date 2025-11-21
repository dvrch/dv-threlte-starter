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
	import { useThrelte, useTick } from '@threlte/core'

	export let height: number = 512;
	export let width: number = 512;
	export let mipmapBlur: boolean = true;

	const { scene, renderer, camera } = useThrelte()
	const composer = new EffectComposer(renderer)

	const setupEffectComposer = (camera: THREE.Camera) => {
		composer.removeAllPasses()
		composer.addPass(new RenderPass(scene, camera))
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

	useTick((_, delta) => {
		composer.render(delta)
	})
</script>