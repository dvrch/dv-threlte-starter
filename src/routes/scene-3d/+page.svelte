<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { Grid } from '@threlte/extras';
	import InteractivitySetup from '$lib/InteractivitySetup.svelte';
	import GltfModel from '$lib/components/GltfModel.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div>
	<Canvas renderMode="always">
		<InteractivitySetup>
			<T.DirectionalLight castShadow position={[3, 10, 10]} intensity={1.5} />
			<T.AmbientLight intensity={0.5} />

			{#if data.error}
				<p>{data.error}</p>
			{:else}
				{#each data.geometries as geometry (geometry.id)}
					{#if geometry.model_url}
						<GltfModel
							url={geometry.model_url}
							position={[geometry.position.x, geometry.position.y, geometry.position.z]}
							rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
							scale={geometry.scale
								? [geometry.scale.x, geometry.scale.y, geometry.scale.z]
								: [1, 1, 1]}
						/>
					{/if}
				{/each}
			{/if}

			<Grid />
		</InteractivitySetup>
	</Canvas>
</div>

<style>
	div {
		height: 100vh;
		width: 100vw;
	}
</style>
