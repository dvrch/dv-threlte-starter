<script lang="ts">
	import TextScene from '../../routes/Text/scene.svelte';
	// @ts-ignore
	import cvContent from '../../routes/Text/cv-en.md?raw';

	let { cvLines = [] }: { cvLines: string[] } = $props();

	// Si cvLines n'est pas fourni par le parent, on utilise l'import direct 🎯
	let finalLines = $derived(
		cvLines.length > 0
			? cvLines
			: cvContent.split('\n').filter((line: string) => line.trim() !== '')
	);
</script>

<TextScene cvLines={finalLines} />
