<script lang="ts">
	import { useThrelte } from '@threlte/core';
	import { PMREMGenerator, LessEqualDepth, Color } from 'three';
	import { onMount, onDestroy } from 'svelte';

	const { scene, renderer } = useThrelte();

	let pmrem = new PMREMGenerator(renderer);
	let dynamicEnvMap: any = null;

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

		// 2. High-end Reflections - Strong intensity
		material.envMapIntensity = 3.0;

		// 3. Iridescence (The "Colored/Multicolor" look users liked)
		// This adds the rainbow sheen oil-slick effect
		if ('iridescence' in material) material.iridescence = 1.0;
		if ('iridescenceIOR' in material) material.iridescenceIOR = 1.3;
		if ('iridescenceThicknessRange' in material) material.iridescenceThicknessRange = [100, 400];

		// 4. Glassy/Metallic polish
		if ('roughness' in material) material.roughness = Math.min(material.roughness || 0.5, 0.05);
		if ('metalness' in material) material.metalness = Math.max(material.metalness || 0, 0.8);

		if (envTexture) {
			material.envMap = envTexture;
		}

		// 5. Emissive Boost
		if ('emissiveIntensity' in material) {
			if (
				material.emissive &&
				(material.emissive.r > 0.1 || material.emissive.g > 0.1 || material.emissive.b > 0.1)
			) {
				material.emissiveIntensity = Math.max(material.emissiveIntensity, 5.0);
			}
		}

		material.needsUpdate = true;
	}

	function refreshSceneMaterials() {
		if (!scene) return;

		// Use the global HDR environment instead of dynamic capture (which causes black screens)
		const texture = scene.environment || null;

		scene.traverse((child: any) => {
			if (child.isMesh && child.material) {
				if (Array.isArray(child.material)) {
					child.material.forEach((m: any) => applyPremiumToMaterial(m, texture, child));
				} else {
					applyPremiumToMaterial(child.material, texture, child);
				}
			}
		});
	}

	// Replaced "captureEnvironment" with a safe refresh
	// We no longer use pmrem.fromScene as it causes the "everything black" loop
	const safeRefresh = () => {
		if (!renderer || !scene) return;
		refreshSceneMaterials();
	};

	onMount(() => {
		// Apply immediately and then periodically to catch new objects
		const timeout = setTimeout(safeRefresh, 500);
		const interval = setInterval(safeRefresh, 2000); // reduced frequency

		return () => {
			clearTimeout(timeout);
			clearInterval(interval);
		};
	});

	onDestroy(() => {
		// Cleanup if needed
	});
</script>
