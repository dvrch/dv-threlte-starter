<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { onMount, onDestroy } from 'svelte';
	import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
	import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
	import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
	import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';

	export let strength = 0.5;
	export let radius = 0.5;
	export let threshold = 0.0;

	const { scene, camera, renderer } = useThrelte();

	let composer: EffectComposer;
	let renderPass: RenderPass;
	let bloomPass: UnrealBloomPass;
	let outputPass: OutputPass;

	onMount(() => {
		composer = new EffectComposer(renderer);
		composer.setPixelRatio(window.devicePixelRatio);
		composer.setSize(window.innerWidth, window.innerHeight);

		renderPass = new RenderPass(scene, camera.current);
		composer.addPass(renderPass);

		bloomPass = new UnrealBloomPass(
			new THREE.Vector2(window.innerWidth, window.innerHeight),
			strength,
			radius,
			threshold
		);
		composer.addPass(bloomPass);

		outputPass = new OutputPass();
		composer.addPass(outputPass);

		// Override Threlte's default render loop
		renderer.setAnimationLoop(() => {
			composer.render();
		});
	});

	onDestroy(() => {
		renderer.setAnimationLoop(null); // Restore default render loop
		composer.dispose();
		renderPass.dispose();
		bloomPass.dispose();
		outputPass.dispose();
	});

	// Reactive updates for bloom properties
	$effect(() => {
		if (bloomPass) {
			bloomPass.strength = strength;
			bloomPass.radius = radius;
			bloomPass.threshold = threshold;
		}
	});
</script>

<!-- No HTML needed for post-processing effects -->
