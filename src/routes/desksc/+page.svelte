

<!-- <Canvas>
	<Scene />
	<Vague />
</Canvas> -->



<script>
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	
	let Canvas = $state(null);
	let Scene = $state(null);
	
	onMount(async () => {
		if (browser) {
			const module = await import('./scene.svelte');
			Scene = module.default;
			
			const threlte = await import('@threlte/core');
			Canvas = threlte.Canvas;
		}
	});
</script>

{#if browser && Canvas && Scene}
	<Canvas>
		<Scene />
	</Canvas>
{/if}





<!-- <div class="div">
	<Vague />
</div> 
 
<style>
	.div {position: absolute; 
		top: 0; 
		left: 0; 
		width: 100%; 
		height: 100%; 
		z-index: -2;
		transform: scale(1.2);
		transition: transform 0.5s ease; 
	}
	.div:hover {transform: scale(0.1);}
</style>
 -->
