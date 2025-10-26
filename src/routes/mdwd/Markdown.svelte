<script>
    import { onMount } from 'svelte';
    import { marked } from 'marked';
    
    let content = '';

    onMount(async () => {
        const response = await fetch('/src/routes/mdwd/Montage de projet Djontso victorien 15_08_2O24.md');
        if (!response.ok) {
            console.error('Erreur lors du chargement du fichier:', response.statusText);
            return;
        }
        const text = await response.text();
        content = marked(text);
    });
</script>

<div class="markdown-content">
    {@html content}
</div>

<style>
    .markdown-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        line-height: 1.6;
    }

    .markdown-content :global(h1), 
    .markdown-content :global(h2), 
    .markdown-content :global(h3), 
    .markdown-content :global(h4), 
    .markdown-content :global(h5), 
    .markdown-content :global(h6) {
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }

    .markdown-content :global(p) {
        margin-bottom: 1em;
    }

    .markdown-content :global(ul), 
    .markdown-content :global(ol) {
        margin-bottom: 1em;
        padding-left: 2em;
    }

    .markdown-content :global(table) {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 1em;
    }

    .markdown-content :global(th), 
    .markdown-content :global(td) {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }

    .markdown-content :global(th) {
        background-color: #f2f2f2;
    }

    .markdown-content :global(img) {
        max-width: 100%;
        height: auto;
    }
</style>
