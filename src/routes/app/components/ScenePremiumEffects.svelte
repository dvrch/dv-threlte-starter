<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { Environment } from '@threlte/extras';
	import { onMount, onDestroy } from 'svelte';

	const { scene } = useThrelte();

	function applyPremiumToMaterial(material: any, envTexture: any, object: any) {
		if (!material) return;

		const name = (object.name || '').toLowerCase();
		if (name.includes('star') || name.includes('sky') || name.includes('grid')) return;

		// Use scene.environment (HDR preset) - stable and never black
		if (envTexture) {
			material.envMap = envTexture;
			material.envMapIntensity = 3.0;
		}

		if (!material.metalnessMap && 'metalness' in material) {
			material.metalness = Math.max(material.metalness || 0, 0.6);
		}
		if (!material.roughnessMap && 'roughness' in material) {
			material.roughness = Math.min(material.roughness || 0.5, 0.08);
		}

		if ('iridescence' in material) material.iridescence = 1.0;
		if ('iridescenceIOR' in material) material.iridescenceIOR = 1.3;
		if ('iridescenceThicknessRange' in material) material.iridescenceThicknessRange = [100, 400];

		if ('emissiveIntensity' in material) {
			if (
				material.emissive &&
				(material.emissive.r > 0 || material.emissive.g > 0 || material.emissive.b > 0)
			) {
				material.emissiveIntensity = 12.0;
			}
		}

		material.needsUpdate = true;
	}

	function refreshSceneMaterials() {
		if (!scene) return;

		const texture = scene.environment;

		// If texture is null, it means HDR hasn't loaded yet.
		// We shouldn't apply "null" as it removes reflections.
		// Just wait for the next check.
		if (!texture) return;

		scene.traverse((child: any) => {
			if (child.isMesh && child.material) {
				const materials = Array.isArray(child.material) ? child.material : [child.material];
				materials.forEach((mat: any) => applyPremiumToMaterial(mat, texture, child));
			}
		});
	}

	onMount(() => {
		// Try immediately
		refreshSceneMaterials();

		// Retry loop: crucial because HDR loads asynchronously from the web
		const interval = setInterval(() => {
			if (scene.environment) {
				refreshSceneMaterials();
				// CRITICAL: Stop checking once found to save performance
				clearInterval(interval);
			}
		}, 1000);

		// Also refresh when new models are added
		const handleRefresh = () => setTimeout(refreshSceneMaterials, 100);
		window.addEventListener('modelAdded', handleRefresh);
		window.addEventListener('modelVisualLoaded', handleRefresh);

		return () => {
			clearInterval(interval);
			window.removeEventListener('modelAdded', handleRefresh);
			window.removeEventListener('modelVisualLoaded', handleRefresh);
		};
	});

	onDestroy(() => {
		// No cleanup needed
	});
</script>

<Environment url="/models/compos-hdr/hdrpersOutput.hdr" isBackground={false} />
