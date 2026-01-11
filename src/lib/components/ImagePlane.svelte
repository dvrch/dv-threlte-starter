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

	// 🎨 Texture Loading (Reactive String -> Store)
	// On évite Cloudinary pour les URLs locaux (blob)
	const imageUrl = $derived(geometry?.model_url || '');

	const texture = useTexture(imageUrl);
</script>

{#if $texture}
	<T.Mesh>
		<T.PlaneGeometry args={[1, 1]} />
		<T.MeshBasicMaterial map={$texture} transparent={true} side={DoubleSide} toneMapped={false} />
	</T.Mesh>
{:else}
	<T.Mesh>
		<T.PlaneGeometry args={[1, 1]} />
		<T.MeshBasicMaterial color="#333" wireframe opacity={0.3} transparent />
	</T.Mesh>
{/if}
