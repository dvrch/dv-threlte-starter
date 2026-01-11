<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { useGltf, useTexture } from '@threlte/extras';
	import { DoubleSide } from 'three';
	import * as THREE from 'three';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';

	interface Props {
		geometry: {
			model_url?: string;
			name?: string;
			color?: string;
		};
	}

	let { geometry }: Props = $props();

	let model = $state<THREE.Group | null>(null);
	let mixer = $state<THREE.AnimationMixer | null>(null);
	let clock = new THREE.Clock();
	let resolvedGltfUrl = $state<string>('');

	const imageUrl = $derived(geometry?.model_url || '');
	const texture = useTexture(imageUrl);

	onMount(async () => {
		if (!browser) return;

		resolvedGltfUrl = await getWorkingAssetUrl('cloth_sim.glb', 'models');
		const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js');
		const loader = new GLTFLoader();

		loader.load(resolvedGltfUrl, (gltf) => {
			buildSceneGraph(gltf);
			model = gltf.scene;
			if (gltf.animations.length > 0) {
				mixer = new THREE.AnimationMixer(model);
				const action = mixer.clipAction(gltf.animations[0]);
				action.play();
			}
		});

		window.addEventListener('modelAdded', () => {
			/* refresh logic if needed */
		});
	});

	$effect(() => {
		if (model && $texture) {
			model.traverse((child: any) => {
				if (child.isMesh) {
					child.material = new THREE.MeshBasicMaterial({
						map: $texture,
						transparent: true,
						side: DoubleSide,
						toneMapped: false
					});
				}
			});
		}
	});

	useTask(() => {
		if (mixer) {
			const delta = clock.getDelta();
			mixer.update(delta);
		}
	});
</script>

{#if model}
	<T is={model} />
{:else}
	<T.Mesh>
		<T.BoxGeometry args={[0.5, 0.5, 0.5]} />
		<T.MeshBasicMaterial color="#333" wireframe opacity={0.3} transparent />
	</T.Mesh>
{/if}
