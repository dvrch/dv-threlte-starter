<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { PMREMGenerator, LessEqualDepth } from 'three';
	import { onMount, onDestroy } from 'svelte';

	const { scene, renderer } = useThrelte();

	let pmrem = new PMREMGenerator(renderer);
	let dynamicEnvMap: any = null;

	function applyPremiumToMaterial(material: any, envTexture: any) {
		if (!material) return;

		// Sane defaults for high-quality rendering
		material.transparent = material.opacity < 1;
		material.depthWrite = true;

		// Controlled settings - balanced for "Day" lighting
		material.envMapIntensity = 1.5; // Back to a sane value (was 100)
		if ('roughness' in material) {
			// Don't override if already very low, but provide a good default
			material.roughness = Math.max(material.roughness, 0.15);
		}
		if ('metalness' in material) {
			material.metalness = Math.min(material.metalness, 0.8);
		}

		if (envTexture) {
			material.envMap = envTexture;
		} else if (scene.environment) {
			material.envMap = scene.environment;
		}

		// Glow boost for emissive materials - more subtle
		if ('emissiveIntensity' in material && material.emissiveIntensity > 0) {
			material.emissiveIntensity = 2.0; // Sane glow (was 20)
		}

		material.needsUpdate = true;
	}

	function refreshSceneMaterials() {
		if (!scene) return;

		const texture = dynamicEnvMap ? dynamicEnvMap.texture : scene.environment;

		scene.traverse((child: any) => {
			if (child.isMesh && child.material) {
				if (Array.isArray(child.material)) {
					child.material.forEach((m: any) => applyPremiumToMaterial(m, texture));
				} else {
					applyPremiumToMaterial(child.material, texture);
				}
			}
		});
	}

	const captureEnvironment = () => {
		if (!renderer || !scene) return;

		if (dynamicEnvMap) dynamicEnvMap.dispose();
		// Capture scene to allow reflections of stars and light
		dynamicEnvMap = pmrem.fromScene(scene, 0, 0.1, 1000);

		refreshSceneMaterials();
	};

	onMount(() => {
		// Run once after models load
		const timeout = setTimeout(captureEnvironment, 1000);
		// Periodically refresh to catch dynamic movement (less frequent)
		const interval = setInterval(captureEnvironment, 5000);
		return () => {
			clearTimeout(timeout);
			clearInterval(interval);
		};
	});

	onDestroy(() => {
		if (dynamicEnvMap) dynamicEnvMap.dispose();
		pmrem.dispose();
	});
</script>
