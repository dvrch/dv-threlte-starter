<script>
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls, Grid } from '@threlte/extras';
	import { degToRad } from 'three/src/math/MathUtils';
	import InteractivitySetup from '$lib/InteractivitySetup.svelte';
	import GltfModel from '$lib/components/GltfModel.svelte';

	export let data;
</script>


<div>
	<Canvas>
		<InteractivitySetup />
		<T.PerspectiveCamera makeDefault position={[10, 10, 10]} fov={24}>
			{#if browser}
				<OrbitControls maxPolarAngle={degToRad(80)} target={{ y: 0.5 }} />
			{/if}
		</T.PerspectiveCamera>

		<T.DirectionalLight castShadow position={[3, 10, 10]} intensity={1.5} />
		<T.AmbientLight intensity={0.5} />

		{#if data.error}
			<p>{data.error}</p>
		{:else}
			{#each data.geometries as geometry (geometry.id)}
				{#if geometry.model_url}
					<GltfModel 
						url={geometry.model_url} 
						position={geometry.position}
						rotation={geometry.rotation}
					/>
				{/if}
			{/each}
		{/if}

		<Grid />

	</Canvas>
</div>

<style>
	div {
		height: 100vh;
		width: 100vw;
	}
</style>100vw;
	}
</style>