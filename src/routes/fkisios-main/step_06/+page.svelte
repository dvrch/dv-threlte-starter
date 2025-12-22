<script>
	import { onMount } from 'svelte';
	import App from './app.svelte';
</script>

<main>
	<App />
	<canvas />
</main>

<style>
	main {
		position: relative;
		width: 100%;
		height: 100vh;
	}
	canvas {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -1;
	}
</style>
