<script lang="ts">
	import {
		BloomEffect,
		EffectComposer,
		EffectPass,
		KernelSize,
		RenderPass,
		SMAAEffect,
		SMAAPreset,
		ChromaticAberrationEffect,
		VignetteEffect
	} from 'postprocessing';
	import { useThrelte, useTask } from '@threlte/core';
	import * as THREE from 'three';
	import { onMount } from 'svelte';

	let {
		intensity = 1.0, // Slightly more pronounced bloom
		luminanceThreshold = 0.2, // More sensitive to light
		height = 1024,
		width = 1024,
		luminanceSmoothing = 0.1,
		mipmapBlur = true
	} = $props();

	const { scene, renderer, camera, autoRender, renderStage, size } = useThrelte();
	const composer = new EffectComposer(renderer);

	// Threlte 8 + Svelte 5 handling: camera can be a store or a direct ref.
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
				}),
				new ChromaticAberrationEffect({
					offset: new THREE.Vector2(0.001, 0.001),
					radialModulation: false,
					modulationOffset: 0
				}),
				new VignetteEffect({
					eskil: false,
					offset: 0.35,
					darkness: 0.5
				}),
				new SMAAEffect({
					preset: SMAAPreset.HIGH
				})
			)
		);
	}

	// Dynamic resizing
	$effect(() => {
		composer.setSize(size.current.width, size.current.height);
	});

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

	// Handle Threlte rendering
	$effect(() => {
		const initialAutoRender = autoRender.current;
		autoRender.set(false);
		return () => {
			autoRender.set(initialAutoRender);
		};
	});

	// Workaround for initialization glitches: brief delay before rendering
	let ready = $state(false);
	onMount(() => {
		const timer = setTimeout(() => {
			ready = true;
		}, 100);
		return () => clearTimeout(timer);
	});

	useTask(
		(delta) => {
			if (!ready || !composer || !currentCamera || composer.passes.length < 2) return;
			composer.render(delta);
		},
		{ stage: renderStage }
	);
</script>
