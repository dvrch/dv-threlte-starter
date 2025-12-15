<script lang="ts">
	import { Canvas } from '@threlte/core';
	import { browser } from '$app/environment';
	import Scene from './Scene.svelte';
	import './styles.css';

	let sceneInstance = $state<Scene | null>(null);
</script>

{#if browser}
	<Canvas>
		<Scene bind:this={sceneInstance} />
	</Canvas>

	<div class="controls">
		<button onclick={() => sceneInstance?.nextTexture()}>Change Texture</button>
	</div>
{/if}

<style>
	.controls {
		position: absolute;
		top: 10px;
		left: 10px;
		z-index: 10;
	}
	button {
		padding: 10px;
		font-size: 16px;
	}
</style>
