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
	// 🎨 Texture Loading (Reactive String -> Store)
	// useTexture accepte une rune $derived directement dans Svelte 5 / Threlte
	const texture = useTexture(() => geometry?.model_url || '');
</script>

{#if $texture}
	<T.Mesh>
		<T.PlaneGeometry args={[1, 1]} />
		<T.MeshBasicMaterial map={$texture} transparent={true} side={DoubleSide} toneMapped={false} />
	</T.Mesh>
{:else}
	<T.Mesh>
		<T.PlaneGeometry args={[1, 1]} />
		<T.MeshBasicMaterial color={geometry?.color || '#4db6ac'} wireframe opacity={0.5} transparent />
		<HTML center>
			<div style="color: white; font-size: 8px; background: rgba(0,0,0,0.5); padding: 2px;">
				Loading Image...
			</div>
		</HTML>
	</T.Mesh>
{/if}
