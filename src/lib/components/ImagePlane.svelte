<script lang="ts">
	import { T, useLoader } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import { TextureLoader, MeshStandardMaterial, DoubleSide, sRGBEncoding } from 'three';
	import * as THREE from 'three';
	import { getCloudinaryAssetUrl, buildSceneGraph } from '$lib/utils/cloudinaryAssets';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';

	interface Props {
		geometry: {
			model_url?: string;
			name?: string;
			color?: string;
		};
	}

	let { geometry }: Props = $props();

	// 🎨 Use Cloudinary URL for the uploaded image
	const imageUrl = $derived(() => {
		const rawUrl = geometry?.model_url;
		if (!rawUrl) return null;
		return getCloudinaryAssetUrl(rawUrl, 'dv-threlte/models');
	});

	const loader = useLoader(TextureLoader);
	const textureStore = $derived(imageUrl() ? loader.load(imageUrl()!) : null);

	// 🧵 Load the exact same cloth_sim.glb as in the tissus-simulat component
	// This provides the draped/folded geometry the user wants
	const glbUrlPromise = getWorkingAssetUrl('cloth_sim.glb', 'models');
	const gltf = useGltf(glbUrlPromise);

	// 🛠️ Apply the uploaded texture to the cloth model
	$effect(() => {
		if ($gltf && $textureStore) {
			const tex = $textureStore as THREE.Texture;

			// In Threlte/Three, we want to ensure materials are updated when the texture arrives
			$gltf.scene.traverse((child) => {
				if ((child as any).isMesh) {
					const mesh = child as THREE.Mesh;
					mesh.material = new MeshStandardMaterial({
						map: tex,
						transparent: true,
						side: DoubleSide,
						roughness: 0.5,
						metalness: 0.1
					});
				}
			});

			// Security/Fix for Cloudinary assets
			buildSceneGraph($gltf);
		}
	});
</script>

<!-- The model handles its own internal geometry. We just render it. -->
{#if $gltf}
	<T is={$gltf.scene} />
{:else}
	<!-- Minimal placeholder while loading -->
	<T.Mesh position={[0, 0, 0.02]}>
		<T.PlaneGeometry args={[1, 1]} />
		<T.MeshBasicMaterial color="#333333" transparent opacity={0.5} />
	</T.Mesh>
{/if}
