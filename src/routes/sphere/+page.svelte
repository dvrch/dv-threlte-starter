<script lang="ts">
	import Scene from './Scene.svelte';
	import './styles.css';

	let sceneInstance: Scene;
</script>

<Scene bind:this={sceneInstance} />

<div class="controls">
	<button onclick={() => sceneInstance?.nextTexture()}>Change Texture</button>
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
