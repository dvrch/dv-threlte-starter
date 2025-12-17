<script lang="ts">
	import { T } from '@threlte/core';
	import { OrbitControls, useGltf } from '@threlte/extras';
	import Bloom from './bloom.svelte';
	import Vague from './vague.svelte';
	import { browser } from '$app/environment';
	import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';

	// let y = 2;
	// let rotation = 0;

	const modelNames = [
		getCloudinaryAssetUrl('/models/ghost.glb'),
		getCloudinaryAssetUrl('/models/Desk-bati.glb'),
		getCloudinaryAssetUrl('cloth_sim.glb')
	];

	// function levitate() {
	// 	const time = Date.now() / 1000;
	// 	const speed = 1;
	// 	const offset = 3;
	// 	y = Math.sin(time * speed) + offset;
	// 	requestAnimationFrame(levitate);
	// }

	// useFrame((_, delta) => {
	// 	rotation += delta * 0.4;
	// });

	// levitate();
</script>

{#if browser}
	<Bloom />
	<T.AmbientLight color="#ffffff" intensity={10} />
	<T.PointLight intensity={10} position={[1, 2, -4]} color="#76aac8" />
{/if}

{#if browser}
	{#await Promise.all(modelNames.map((url) => useGltf(url))) then results}
		{#each results as result}
			<T is={result.scene} position={[0, 0, 0]} scale={0.4} />
		{/each}
		<!-- <T is={results[0].scene} rotation.y={0} levitate()/>
	<T is={results[1].scene} rotation.y={0} />
	<T is={results[2].scene} rotation.y={0} levitate()/> -->
	{/await}
{:else}
	<!-- Placeholder for SSR if needed, or just render nothing -->
{/if}

{#if browser}
	<div class="div">
		<Vague />
	</div>
{/if}

<style>
	.div {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: 2;
	}
</style>
