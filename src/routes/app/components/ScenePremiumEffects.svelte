<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { LessEqualDepth, Color } from 'three';
	import { onMount, onDestroy } from 'svelte';

	import Bloom from '../models/bloom.svelte';

	const { scene, renderer } = useThrelte();

	function applyPremiumToMaterial(material: any, envTexture: any, object: any) {
		if (!material) return;

		const name = (object.name || '').toLowerCase();
		// skip environment and helpers/gizmos
		if (
			name.includes('star') ||
			name.includes('sky') ||
			name.includes('galaxy') ||
			name.includes('grid') ||
			name.includes('gizmo') ||
			name.includes('transform') ||
			name.includes('helper') ||
			name.includes('bone')
		)
			return;

		// 1. Better visibility for dark objects
		if (material.color) {
			const col = material.color;
			// If color is black or very dark, give it a subtle emissive boost so it doesn't vanish
			if (col.r < 0.02 && col.g < 0.02 && col.b < 0.02) {
				if (material.emissive && material.emissive.r === 0) {
					// Sublest blueish hue for dark materials to feel high-end
					material.emissive.setHex(0x111122);
					material.emissiveIntensity = 0.5;
				}
			}
		}

		// 2. High-end Reflections - Boosted for premium feel
		material.envMapIntensity = 3.0;

		if (envTexture) {
			material.envMap = envTexture;
		}

		// 3. Emissive Boost (The "Glow" effect) - Stronger
		if ('emissiveIntensity' in material) {
			if (
				material.emissive &&
				(material.emissive.r > 0.1 || material.emissive.g > 0.1 || material.emissive.b > 0.1)
			) {
				material.emissiveIntensity = Math.max(material.emissiveIntensity, 10.0);
			}
		}

		material.needsUpdate = true;
	}

	function refreshSceneMaterials() {
		if (!scene) return;
		scene.traverse((child: any) => {
			if (child.isMesh && child.material) {
				const texture = scene.environment; // Use global environment
				if (Array.isArray(child.material)) {
					child.material.forEach((m: any) => applyPremiumToMaterial(m, texture, child));
				} else {
					applyPremiumToMaterial(child.material, texture, child);
				}
			}
		});
	}

	onMount(() => {
		// Just run once after a delay to ensure assets are loaded
		const timeout = setTimeout(refreshSceneMaterials, 1000);
		// Listen for modelAdded (new item) AND modelVisualLoaded (visual ready) to refresh
		const handleModelRefresh = () => setTimeout(refreshSceneMaterials, 500);

		window.addEventListener('modelAdded', handleModelRefresh);
		window.addEventListener('modelVisualLoaded', handleModelRefresh);

		return () => {
			clearTimeout(timeout);
			window.removeEventListener('modelAdded', handleModelRefresh);
			window.removeEventListener('modelVisualLoaded', handleModelRefresh);
		};
	});
</script>

<Bloom />
