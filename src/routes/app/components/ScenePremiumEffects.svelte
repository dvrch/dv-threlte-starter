<script lang="ts">
	import { useThrelte, useLoader } from '@threlte/core';
	import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';
	import { onMount, onDestroy } from 'svelte';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';

	const { scene } = useThrelte();

	// Use Cloudinary URL for HDR
	const hdrUrl = getCloudinaryAssetUrl(
		'compos-hdr/hdrpersOutput.hdr',
		'dv-threlte/models/compos-hdr'
	);

	const hdrTexture = useLoader(RGBELoader, () => hdrUrl);

	$effect(() => {
		if (hdrTexture.current) {
			scene.environment = hdrTexture.current;
			// Immediate refresh when texture arrives
			refreshSceneMaterials();
		}
	});

	function applyPremiumToMaterial(material: any, envTexture: any, object: any) {
		if (!material) return;

		const name = (object.name || '').toLowerCase();
		if (name.includes('star') || name.includes('sky') || name.includes('grid')) return;

		// Skip MeshBasicMaterial (used for images/planes) - they don't need env maps
		if (material.isMeshBasicMaterial) return;

		// Use scene.environment (HDR preset) - stable and never black
		if (envTexture) {
			material.envMap = envTexture;
			material.envMapIntensity = 0.8; // Reduced intensity
		}

		if (!material.metalnessMap && 'metalness' in material) {
			// Only make materials more metallic if they are not completely non-metallic
			if (material.metalness > 0.1) {
				material.metalness = Math.max(material.metalness, 0.5);
			}
		}
		if (!material.roughnessMap && 'roughness' in material) {
			material.roughness = Math.min(material.roughness || 0.5, 0.15); // Made it less mirror-like
		}

		if ('iridescence' in material) material.iridescence = 1.0;
		if ('iridescenceIOR' in material) material.iridescenceIOR = 1.3;
		if ('iridescenceThicknessRange' in material) material.iridescenceThicknessRange = [100, 400];

		if ('emissiveIntensity' in material) {
			if (
				material.emissive &&
				(material.emissive.r > 0 || material.emissive.g > 0 || material.emissive.b > 0)
			) {
				material.emissiveIntensity = 0.8; // Reduced intensity
			}
		}

		// Force material recompilation/update by toggling a property
		// This simulates the user's observed "on-off-on" cycle
		material.needsUpdate = false; // Temporarily set to false
		setTimeout(() => {
			material.needsUpdate = true; // Then set to true after a tiny delay
		}, 10); // Small delay to ensure Three.js registers the "change"
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
			}
		}, 500); // Faster check initially

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
