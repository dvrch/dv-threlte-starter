<script lang="ts">
	import { useThrelte, useTask } from '@threlte/core';
	import { PMREMGenerator, LessEqualDepth } from 'three';
	import { onMount, onDestroy } from 'svelte';
	import Bloom from '../models/bloom.svelte';

	const { scene, renderer } = useThrelte();

	let pmrem = new PMREMGenerator(renderer);
	let dynamicEnvMap: any = null;

	function applyPremiumToMaterial(material: any, envTexture: any) {
		if (!material) return;

		// Ensure standard material properties for reflections
		material.depthFunc = LessEqualDepth;
		material.depthTest = true;
		material.depthWrite = true;

		// Premium settings
		// DOUBLED INTENSITY: Very strong reflections
		material.envMapIntensity = 5.0;

		// Intelligent Polish: Make things shiny but NOT pure black mirrors
		if ('roughness' in material) {
			// almost perfect mirror (0.02)
			material.roughness = Math.min(material.roughness || 0.5, 0.02);
		}
		if ('metalness' in material) {
			// Very metallic (0.85) for crisp reflections
			material.metalness = Math.max(material.metalness || 0, 0.85);
		}
		if ('clearcoat' in material) material.clearcoat = 1.0; // Extra polish layer
		if ('clearcoatRoughness' in material) material.clearcoatRoughness = 0.0;

		// "CLAIRE MULTICOLOR" -> Iridescence (Rainbow/Soap-bubble effect)
		// This adds the requested multicolor sheen
		if ('iridescence' in material) material.iridescence = 1.0;
		if ('iridescenceIOR' in material) material.iridescenceIOR = 1.5;
		if ('iridescenceThicknessRange' in material) material.iridescenceThicknessRange = [100, 800];

		if (envTexture) {
			material.envMap = envTexture;
		} else if (scene.environment) {
			material.envMap = scene.environment;
		}

		// Glow boost for emissive materials
		if ('emissiveIntensity' in material) {
			material.emissiveIntensity = 4;
		}

		material.needsUpdate = true;
	}

	function refreshSceneMaterials() {
		if (!scene) return;

		const texture = dynamicEnvMap ? dynamicEnvMap.texture : scene.environment;

		scene.traverse((child: any) => {
			// Skip UI/Helpers to avoid weird artifacts
			if (
				child.name.includes('gizmo') ||
				child.name.includes('helper') ||
				child.name.includes('grid')
			)
				return;

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
		dynamicEnvMap = pmrem.fromScene(scene, 0, 0.1, 1000);

		refreshSceneMaterials();
	};

	onMount(() => {
		// Rely on the scene's global environment (HDR) instead of dynamic capture
		// to avoid "black hole" feedback loops and performance costs.
		// We still apply premium material settings (roughness, metalness) periodically/on-change.

		// Initial application
		setTimeout(refreshSceneMaterials, 500);

		// Refresh when new models are added
		const handleRefresh = () => setTimeout(refreshSceneMaterials, 100);
		window.addEventListener('modelAdded', handleRefresh);
		window.addEventListener('modelVisualLoaded', handleRefresh);

		// Periodic refresh just in case materials change
		const interval = setInterval(refreshSceneMaterials, 2000);

		return () => {
			clearInterval(interval);
			window.removeEventListener('modelAdded', handleRefresh);
			window.removeEventListener('modelVisualLoaded', handleRefresh);
		};
	});

	onDestroy(() => {
		if (dynamicEnvMap) dynamicEnvMap.dispose();
		pmrem.dispose();
	});
</script>
