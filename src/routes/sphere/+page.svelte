<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import type Scene from './Scene.svelte';
	import './styles.css';

	let Canvas;
	let SceneComponent: typeof Scene;
	let sceneInstance: Scene;

	onMount(async () => {
		if (browser) {
			const threlte = await import('@threlte/core');
			Canvas = threlte.Canvas;
			const module = await import('./Scene.svelte');
			SceneComponent = module.default;
		}
	});
</script>

{#if browser && Canvas && SceneComponent}
	<Canvas>
		<SceneComponent bind:this={sceneInstance} />
	</Canvas>
{/if}

<div class="controls">
	<button on:click={() => sceneInstance?.nextTexture()}>Change Texture</button>
</div>

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
