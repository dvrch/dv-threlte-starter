<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { Environment } from '@threlte/extras';
	import { onMount, onDestroy } from 'svelte';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';
	import { untrack } from 'svelte';

	const { scene } = useThrelte();

	// Use Cloudinary URL for HDR
	const hdrUrl = getCloudinaryAssetUrl('hdrpersOutput.hdr', 'dv-threlte/models/compos-hdr');

	// Re-adopting the working commit 96ec289 logic 🎯
	let isRefreshing = false;

	function applyPremiumToMaterial(material: any, envTexture: any, object: any) {
		if (!material) return;

		const name = (object.name || '').toLowerCase();

		// Skip Background / System objects
		if (name.includes('star') || name.includes('sky') || name.includes('grid')) return;

		// Skip MeshBasicMaterial or specific image planes to avoid "burning" them out
		// Image planes must stay Basic to keep their colors pure
		if (material.isMeshBasicMaterial || name.includes('imageplane')) return;

		// IMPORTANT: Stop if already applied to prevent infinite loops
		// We use the envMap and specific intensity as a marker
		if (material.envMap === envTexture && material.envMapIntensity === 5.0) return;

		if (envTexture) {
			material.envMap = envTexture;
			material.envMapIntensity = 5.0;
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
		if (isRefreshing) return;
		isRefreshing = true;

		const s = scene;
		if (!s || !s.environment) {
			isRefreshing = false;
			return;
		}

		console.log('✨ [PremiumEffects] Refreshing materials...');
		const texture = s.environment;

		s.traverse((child: any) => {
			if (child.isMesh && child.material) {
				const materials = Array.isArray(child.material) ? child.material : [child.material];
				materials.forEach((mat: any) => applyPremiumToMaterial(mat, texture, child));
			}
		});

		isRefreshing = false;
	}

	$effect(() => {
		// Only trigger when environment is ready
		if (scene.environment) {
			untrack(refreshSceneMaterials);
		}
	});

	onMount(() => {
		// Delayed initial refresh
		const timer = setTimeout(() => untrack(refreshSceneMaterials), 1000);

		const handleRefresh = (e: any) => {
			// Debounce or at least delay to let the model settle
			setTimeout(() => untrack(refreshSceneMaterials), 300);
		};

		window.addEventListener('modelAdded', handleRefresh);
		window.addEventListener('modelVisualLoaded', handleRefresh);

		return () => {
			clearTimeout(timer);
			window.removeEventListener('modelAdded', handleRefresh);
			window.removeEventListener('modelVisualLoaded', handleRefresh);
		};
	});
</script>

<Environment url={hdrUrl} isBackground={false} />
