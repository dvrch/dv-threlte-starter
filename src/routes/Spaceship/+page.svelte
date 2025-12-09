<script lang="ts">
	let { position, rotation, scale, data, params } = $props();

	import { browser } from '$app/environment';
 	import { Canvas } from '@threlte/core'
  	import Scene from './Scene.svelte'

	
	let canvas: HTMLCanvasElement ;
</script>


<!-- <div class="div"> -->
	<!-- <Vague /> -->
	<!-- </div> -->
	
		<!-- <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -2;"> -->
			<Canvas renderMode="always">
				{#if browser}
					<Scene />
				{/if}
			</Canvas>
		<!-- </div> -->
		
		
<style>
/* 	
	.div {position: absolute; 
		top: 0; 
		left: 0; 
		width: 100%; 
		height: 100%; 
		z-index: -2;
		transform: scale(1.2);
		transition: transform 0.5s ease; 
	}
	.div:hover {transform: scale(0.1);} */

</style>
