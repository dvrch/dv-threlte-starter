<script lang="ts">
	let { data } = $props();

	import { browser } from '$app/environment';
	import { Canvas } from '@threlte/core';
	import Scene from './Scene.svelte';

	let canvas: HTMLCanvasElement;
</script>

<!-- <div class="div"> -->
<!-- <Vague /> -->
<!-- </div> -->

<div class="canvas-container">
	<Canvas renderMode="always">
		{#if browser}
			<Scene />
		{/if}
	</Canvas>
</div>

<style>
	.canvas-container {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		background: #000;
	}
</style>
