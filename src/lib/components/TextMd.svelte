<script lang="ts">
	import TextScene from '../../routes/Text/scene.svelte';
	import { onMount } from 'svelte';

	let { cvLines = [] }: { cvLines: string[] } = $props();
	let loadedLines = $state<string[]>([]);

	onMount(async () => {
		try {
			// Load cv-en.md content
			const response = await fetch('/Text/cv-en.md');
			const text = await response.text();
			loadedLines = text.split('\n').filter((line) => line.trim() !== '');
		} catch (e) {
			console.error('Failed to load cv-en.md:', e);
			loadedLines = ['# Error loading CV'];
		}
	});
</script>

<TextScene cvLines={loadedLines.length > 0 ? loadedLines : cvLines} />
