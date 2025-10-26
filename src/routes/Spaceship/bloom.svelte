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
	import { useTask, useThrelte } from '@threlte/core'
	import { onMount } from 'svelte';
	import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
	import { Vector2 } from 'three';

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
					height: 512,
					width: 512,
					luminanceSmoothing: 0,
					mipmapBlur: true,
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

	useTask((_, delta) => {
		composer.render(delta)
	})

	export let intensity = 1.5;
	export let luminanceThreshold = 0.9;
	export let luminanceSmoothing = 0.9;
	export let bloomStrength = 1.5;

	onMount(() => {
		const bloomPass = new UnrealBloomPass(
			new Vector2(window.innerWidth, window.innerHeight),
			intensity,
			luminanceThreshold,
			luminanceSmoothing
		);
		bloomPass.strength = bloomStrength;
		
		return () => {
			bloomPass.dispose();
		};
	});
</script>

<!--  -->