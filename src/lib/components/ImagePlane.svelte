<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { DoubleSide } from 'three';
	import * as THREE from 'three';
	import { getCloudinaryAssetUrl, buildSceneGraph } from '$lib/utils/cloudinaryAssets';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';

	interface Props {
		geometry: {
			model_url?: string;
			name?: string;
			color?: string;
		};
	}

	let { geometry }: Props = $props();

	// 🧵 Resolve cloth_sim.glb URL robustly (local or cloudinary fallback)
	let resolvedGltfUrl = $state<string>('');

	onMount(async () => {
		if (browser) {
			resolvedGltfUrl = await getWorkingAssetUrl('cloth_sim.glb', 'models');
		}
	});

	// 🧵 Load cloth_sim.glb reactively
	const gltf = $derived(resolvedGltfUrl ? useGltf(resolvedGltfUrl) : null);

	// 🎨 Texture Loading (Reactive String -> Store)
	const imageUrl = $derived(
		geometry?.model_url ? getCloudinaryAssetUrl(geometry.model_url, 'dv-threlte/models') : ''
	);

	const texture = useTexture(imageUrl);

	// 🛠️ Material Sync
	$effect(() => {
		// Wait for both gltf and texture to be ready
		if (gltf && $gltf && $texture) {
			const currentGltf = $gltf;
			const tex = $texture;

			// Setup texture for pure colors
			if ('colorSpace' in tex) {
				(tex as any).colorSpace = (THREE as any).SRGBColorSpace || 'srgb';
			} else {
				(tex as any).encoding = 3001; // sRGBEncoding value
			}

			tex.flipY = false;
			tex.needsUpdate = true;

			currentGltf.scene.traverse((child: any) => {
				if (child.isMesh) {
					const mesh = child as THREE.Mesh;
					mesh.name = 'imageplane_mesh'; // explicit naming for skip logic in ScenePremiumEffects
					mesh.material = new THREE.MeshBasicMaterial({
						map: tex,
						transparent: true,
						side: DoubleSide,
						toneMapped: false // keep colors absolute and unaffected by tone mapping
					});
				}
			});

			buildSceneGraph(currentGltf);
		}
	});
</script>

<!-- Render the GLTF scene once loaded -->
{#if gltf && $gltf}
	<T is={$gltf.scene} />
{:else}
	<!-- Minimal placeholder while loading -->
	<T.Mesh position={[0, 0, 0.05]}>
		<T.BoxGeometry args={[0.5, 0.5, 0.1]} />
		<T.MeshBasicMaterial color="#333333" wireframe opacity={0.3} transparent />
	</T.Mesh>
{/if}
