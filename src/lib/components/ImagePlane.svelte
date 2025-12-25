<script lang="ts">
	import { T, useLoader } from '@threlte/core';
	import { TextureLoader, DoubleSide } from 'three';
	import * as THREE from 'three';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';

	interface Props {
		geometry: {
			model_url?: string;
			name?: string;
			color?: string;
		};
	}

	let { geometry }: Props = $props();

	const imageUrl = $derived(() => {
		const rawUrl = geometry?.model_url;
		if (!rawUrl) return null;
		return getCloudinaryAssetUrl(rawUrl);
	});

	const loader = useLoader(TextureLoader);
	const textureStore = $derived(imageUrl() ? loader.load(imageUrl()!) : null);

	let aspect = $state(1);

	$effect(() => {
		if (textureStore && $textureStore) {
			const tex = $textureStore as THREE.Texture;

			const checkImage = () => {
				if (tex.image && tex.image.width > 0) {
					aspect = tex.image.width / tex.image.height;
					console.log(`✅ [ImagePlane] Aspect Ready: ${aspect} for ${geometry.name}`);
				}
			};

			checkImage();

			if (!tex.image || tex.image.width === 0) {
				tex.addEventListener('update', checkImage);
				if (tex.source && tex.source.data instanceof HTMLImageElement) {
					tex.source.data.onload = checkImage;
				}
			}

			return () => {
				tex.removeEventListener('update', checkImage);
			};
		}
	});
</script>

<!-- PlaneGeometry faces +Z by default. We scale by aspect ratio. -->
<T.Mesh name="ImagePlaneMesh" scale={[aspect, 1, 1]} position={[0, 0, 0.02]} frustumCulled={false}>
	<T.PlaneGeometry args={[5, 5]} />
	{#if textureStore && $textureStore}
		<T.MeshBasicMaterial
			map={$textureStore as any}
			color="white"
			side={DoubleSide}
			transparent={true}
			toneMapped={false}
			depthWrite={true}
			opacity={1}
		/>
	{:else}
		<!-- Fallback loader / placeholder -->
		<T.MeshBasicMaterial color="#333333" side={DoubleSide} opacity={0.5} transparent={true} />
	{/if}
</T.Mesh>
