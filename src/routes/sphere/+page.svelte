<script lang="ts">
	import { browser } from '$app/environment';
	import Scene from './Scene.svelte';
	import './styles.css';

	let sceneInstance: Scene;
</script>

{#if browser}
	<Scene bind:this={sceneInstance} />

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
