<script lang="ts">
	import { onMount } from 'svelte';
	import {
		BloomEffect,
		EffectComposer,
		EffectPass,
		KernelSize,
		RenderPass,
		SMAAEffect,
		SMAAPreset
	} from 'postprocessing';
	import { T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Stars from '$lib/components/Stars.svelte';
	import Spaceship from '$lib/components/models/spaceship.svelte';
	import Nissan from '$lib/components/Nissan.svelte';

	import { useThrelte, useTask } from '@threlte/core';

	const { renderer, scene, camera } = useThrelte(); // Get renderer, scene, and camera from useThrelte

	let composer: EffectComposer | null = null; // Declare composer here
	let spaceShipRef: any = null;
	let translY = 0;
	let angleZ = 0;
	const cleanupFunctions: (() => void)[] = [];

	const setupEffectComposer = () => {
		if (!renderer || !scene || !camera.current) return; // Ensure they are defined

		if (!composer) {
			// Initialize composer only once
			composer = new EffectComposer(renderer);
			composer.setSize(window.innerWidth, window.innerHeight);
		}

		composer.removeAllPasses();
		composer.addPass(new RenderPass(scene, camera.current));
		composer.addPass(
			new EffectPass(
				camera.current,
				new BloomEffect({
					intensity: 0.8,
					luminanceThreshold: 0,
					height: 512,
					width: 512,
					luminanceSmoothing: 0,
					mipmapBlur: true,
					kernelSize: KernelSize.MEDIUM
				})
			)
		);
		composer.addPass(
			new EffectPass(
				camera.current,
				new SMAAEffect({
					preset: SMAAPreset.LOW
				})
			)
		);
	};

	const setupEnvironmentMapping = () => {
		// Placeholder for environment mapping setup
		// This function was referenced but not defined
	};

	useTask((delta: number) => {
		// Mettre à jour l'environnement et le rendu
		setupEnvironmentMapping();
		if (composer) {
			// Only render if composer is initialized
			composer.render(delta);
		}
	});

	onMount(() => {
		setupEffectComposer();
		setupEnvironmentMapping();

		const interval = setInterval(() => {
			setupEnvironmentMapping();
		}, 1000);

		cleanupFunctions.push(() => {
			clearInterval(interval);
			if (composer) {
				composer.dispose();
			}
		});

		return () => {
			cleanupFunctions.forEach((fn) => fn());
		};
	});
</script>

<div class="div">
	<T.PerspectiveCamera makeDefault position={[-5, 6, 10]} fov={25}>
		<OrbitControls enableDamping target={[0, 0, 0]} />
	</T.PerspectiveCamera>

	<T.DirectionalLight intensity={1.8} position={[0, 10, 0]} castShadow shadow.bias={-0.0001} />

	<Spaceship ref={spaceShipRef} />

	<Stars />

	<Nissan ref={spaceShipRef} />
</div>
