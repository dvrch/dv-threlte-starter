<script lang="ts">
	export let position = [0, 0, 0];
	export let rotation = [0, 0, 0];
	export let scale = 1;
	export let data;
	export let params = {};

	import Bloom from './bloom.svelte';
 	import { Canvas } from '@threlte/core'
  	import Scene from './Scene.svelte'

	
	let canvas: HTMLCanvasElement ;
</script>


<!-- <div class="div"> -->
	<!-- <Vague /> -->
	<!-- </div> -->
	
		<!-- <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -2;"> -->
			<Canvas>
				<Scene />
				<!-- <Bloom /> -->
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
