<script lang="ts">
	import TextScene from '../../routes/Text/scene.svelte';

	// This component now simply accepts cvLines and passes them to the TextScene renderer.
	// All data loading is handled upstream.
	let { cvLines = ['# No content'] }: { cvLines: string[] } = $props();
</script>

<TextScene {cvLines} />
