<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { PMREMGenerator, LessEqualDepth } from 'three';
	import { onMount, onDestroy } from 'svelte';

	const { scene, renderer } = useThrelte();

	let pmrem = new PMREMGenerator(renderer);
	let dynamicEnvMap: any = null;

	function applyPremiumToMaterial(material: any, envTexture: any, objectName: string = '') {
		if (!material) return;

		// 🛑 SKIP environmental objects like Stars to avoid making them black/invisible
		const name = (objectName || '').toLowerCase();
		if (name.includes('star') || name.includes('sky') || name.includes('galaxy')) return;

		// Sane defaults for high-quality rendering
		// We avoid force-setting transparency as it breaks some special shaders
		material.depthWrite = true;

		// Controlled settings - "Premium Middle Ground"
		material.envMapIntensity = 8.0; // Increased from 1.5 (+10% "oomph" feeling)

		if ('roughness' in material) {
			// Keep it shiny but not mirror-like (unless it was already very shiny)
			material.roughness = Math.min(material.roughness, 0.1);
		}
		if ('metalness' in material) {
			material.metalness = Math.max(material.metalness, 0.5);
		}

		if (envTexture) {
			material.envMap = envTexture;
		}

		// Glow boost for emissive materials - more pronounced but not blinding
		if ('emissiveIntensity' in material) {
			// Only boost if it already has some emissive color
			if (
				material.emissive &&
				(material.emissive.r > 0 || material.emissive.g > 0 || material.emissive.b > 0)
			) {
				material.emissiveIntensity = 8.0; // Boosted from 2.0
			}
		}

		material.needsUpdate = true;
	}

	function refreshSceneMaterials() {
		if (!scene) return;

		const texture = dynamicEnvMap ? dynamicEnvMap.texture : scene.environment || null;

		scene.traverse((child: any) => {
			// We only target Meshes. Stars (Points) will be naturally skipped.
			if (child.isMesh && child.material) {
				if (Array.isArray(child.material)) {
					child.material.forEach((m: any) => applyPremiumToMaterial(m, texture, child.name));
				} else {
					applyPremiumToMaterial(child.material, texture, child.name);
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
