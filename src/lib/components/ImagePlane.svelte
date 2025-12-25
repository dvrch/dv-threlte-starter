<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { MeshStandardMaterial, DoubleSide } from 'three';
	import * as THREE from 'three';
	import { getCloudinaryAssetUrl, buildSceneGraph } from '$lib/utils/cloudinaryAssets';

	interface Props {
		geometry: {
			model_url?: string;
			name?: string;
			color?: string;
		};
	}

	let { geometry }: Props = $props();

	// 🎨 Texture Loading (Reactive String -> Store)
	// No function closure here to keep it strictly reactive in Svelte 5
	const imageUrl = $derived(
		geometry?.model_url ? getCloudinaryAssetUrl(geometry.model_url, 'dv-threlte/models') : ''
	);

	// useTexture returns a store (Writable) or AsyncWritable
	const texture = useTexture(imageUrl);

	// 🧵 Load cloth_sim.glb
	// We use the absolute path in static/models/
	const gltf = useGltf('/models/cloth_sim.glb');

	// 🛠️ Material Sync
	$effect(() => {
		// We use untrack or guard to avoid re-triggering effects if necessary,
		// but here we want to update materials whenever gltf or texture changes.
		if ($gltf && $texture) {
			const tex = $texture;
			// sRGBEncoding is the old constant, but it's still available in some THREE namespaces
			// or we use tex.colorSpace = THREE.SRGBColorSpace in newer THREE
			if ('colorSpace' in tex) {
				(tex as any).colorSpace = (THREE as any).SRGBColorSpace;
			} else {
				(tex as any).encoding = 3001; // sRGBEncoding value
			}

			tex.flipY = false;
			tex.needsUpdate = true;

			$gltf.scene.traverse((child) => {
				if ((child as any).isMesh) {
					const mesh = child as THREE.Mesh;
					mesh.material = new MeshStandardMaterial({
						map: tex,
						transparent: true,
						side: DoubleSide,
						roughness: 0.6,
						metalness: 0.2
					});
				}
			});

			buildSceneGraph($gltf);
		}
	});
</script>

<!-- Render the GLTF scene once loaded -->
{#if $gltf}
	<T is={$gltf.scene} />
{:else}
	<!-- Minimal placeholder while loading -->
	<T.Mesh position={[0, 0, 0.05]}>
		<T.BoxGeometry args={[0.5, 0.5, 0.1]} />
		<T.MeshBasicMaterial color="#333333" wireframe opacity={0.3} transparent />
	</T.Mesh>
{/if}
