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
		// skip environment
		if (
			name.includes('star') ||
			name.includes('sky') ||
			name.includes('galaxy') ||
			name.includes('grid')
		)
			return;

		// 1. Ensure the object is visible by giving it a base emissive if it's totally black
		if (material.color) {
			const col = material.color;
			// If color is black or very dark, and it has no emissive, give it a tiny boost
			if (col.r < 0.05 && col.g < 0.05 && col.b < 0.05) {
				if (
					material.emissive &&
					material.emissive.r === 0 &&
					material.emissive.g === 0 &&
					material.emissive.b === 0
				) {
					// Don't force black objects to be bright, but don't let them be "invisible"
					// Maybe it's a lighting issue. Let's ensure envMap is applied.
				}
			}
		}

		// 2. High-end Reflections (Increased as requested by 10% or more)
		material.envMapIntensity = 10.0; // Boosted

		// Only override if it feels like a 3D model that needs it
		// If it has a metalnessMap, we should probably respect it more
		if (!material.metalnessMap && 'metalness' in material) {
			material.metalness = Math.max(material.metalness, 0.6);
		}
		if (!material.roughnessMap && 'roughness' in material) {
			material.roughness = Math.min(material.roughness, 0.08);
		}

		// Iridescence (multicolor rainbow sheen)
		if ('iridescence' in material) material.iridescence = 1.0;
		if ('iridescenceIOR' in material) material.iridescenceIOR = 1.3;
		if ('iridescenceThicknessRange' in material) material.iridescenceThicknessRange = [100, 400];

		if (envTexture) {
			material.envMap = envTexture;
		}

		// 3. Emissive Boost (The "Glow" effect)
		if ('emissiveIntensity' in material) {
			// If it has emissive color, make it shine
			if (
				material.emissive &&
				(material.emissive.r > 0 || material.emissive.g > 0 || material.emissive.b > 0)
			) {
				material.emissiveIntensity = 12.0; // Stronger glow
			}
		}

		material.needsUpdate = true;
	}

	function refreshSceneMaterials() {
		if (!scene) return;

		const texture = dynamicEnvMap ? dynamicEnvMap.texture : scene.environment || null;

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

	let hasCapture = false; // Prevent multiple captures

	const captureEnvironment = () => {
		if (!renderer || !scene || hasCapture) return;

		// Safety: Only capture if scene has lights (not black)
		const hasLights = scene.children.some(
			(child: any) => child.isLight || child.isDirectionalLight || child.isAmbientLight
		);

		if (!hasLights) {
			console.warn('⚠️ Scene not ready for capture (no lights detected)');
			return;
		}

		try {
			if (dynamicEnvMap) dynamicEnvMap.dispose();
			// Capture scene to allow reflections of stars and light
			dynamicEnvMap = pmrem.fromScene(scene, 0, 0.1, 1000);
			hasCapture = true; // Mark as captured
			console.log('✅ Environment captured successfully');
			refreshSceneMaterials();
		} catch (e) {
			console.error('❌ Environment capture failed:', e);
			// Fallback to scene.environment
			refreshSceneMaterials();
		}
	};

	onMount(() => {
		// Wait 2 seconds for scene to be fully lit before capturing
		const timeout = setTimeout(captureEnvironment, 2000);

		// Refresh materials when new models are added
		const handleRefresh = () => setTimeout(refreshSceneMaterials, 100);
		window.addEventListener('modelAdded', handleRefresh);
		window.addEventListener('modelVisualLoaded', handleRefresh);

		return () => {
			clearTimeout(timeout);
			window.removeEventListener('modelAdded', handleRefresh);
			window.removeEventListener('modelVisualLoaded', handleRefresh);
		};
	});

	onDestroy(() => {
		if (dynamicEnvMap) dynamicEnvMap.dispose();
		pmrem.dispose();
	});
</script>
