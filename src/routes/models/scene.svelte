<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import { browser } from '$app/environment';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { createDracoLoader } from '$lib/utils/draco-loader';
	import { buildSceneGraph } from '$lib/utils/cloudinaryAssets';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';
	import { onMount } from 'svelte';

	let y = $state(2);
	let rotation = $state(0);

	let models = $state({
		ghost: null as any,
		garden: null as any,
		nissan: null as any
	});

	function levitate() {
		const time = Date.now() / 1000;
		const speed = 1;
		const offset = 3;
		y = Math.sin(time * speed) + offset;
		requestAnimationFrame(levitate);
	}

	useTask((delta) => {
		rotation += delta * 0.4;
	});

	onMount(async () => {
		if (browser) {
			levitate();
			const loader = new GLTFLoader();
			loader.setDRACOLoader(createDracoLoader());

			const loadSafe = async (name: string) => {
				try {
					const url = await getWorkingAssetUrl(name, 'models');
					const gltf = await loader.loadAsync(url);
					buildSceneGraph(gltf);
					return gltf.scene;
				} catch (e) {
					console.error(`Safe load failed for ${name}`, e);
					return null;
				}
			};

			models.ghost = await loadSafe('ghost.glb');
			models.garden = await loadSafe('garden1.glb');
			models.nissan = await loadSafe('nissan.glb');
		}
	});
</script>

<T.OrthographicCamera position={[10, 10, 10]} zoom={40} makeDefault>
	<OrbitControls enableDamping />
</T.OrthographicCamera>

<T.PointLight intensity={10} position={[1, 2, -4]} color="#76aac8" />
<T.AmbientLight intensity={0.5} />

{#if models.ghost}
	<T is={models.ghost} position={[0, y, 0]} scale={0.4} />
{/if}

{#if models.garden}
	<T is={models.garden} rotation.y={rotation} />
{/if}

{#if models.nissan}
	<T is={models.nissan} position={[2, y, 1]} scale={0.4} />
{/if}
