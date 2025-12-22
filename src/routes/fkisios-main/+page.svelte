<script>
	import { onMount } from 'svelte';
	import './step_06/app.svelte'; // Importation du fichier app.js

	onMount(() => {
		// Initialisation de la scène ici si nécessaire
		// Vous pouvez ajouter des appels de fonction ou des configurations supplémentaires
	});
</script>

<main>
	<h1>Bienvenue dans la scène</h1>
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
