<script>
    import { onMount } from 'svelte';
    import mammoth from 'mammoth';

    let content = '';

    onMount(async () => {
        const response = await fetch('/src/routes/mdwd/Montage de projet Djontso victorien 15_08_2O24.docx');
        if (!response.ok) {
            console.error('Erreur lors du chargement du fichier:', response.statusText);
            return;
        }

        const arrayBuffer = await response.arrayBuffer();
        mammoth.convertToHtml({ arrayBuffer: arrayBuffer })
            .then(result => {
                content = result.value; // HTML string
            })
            .catch(err => {
                console.error('Error converting document:', err);
            });
    });
</script>

<div class="word-content">
    {@html content}
</div>

<style>
    .word-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        line-height: 1.6;
    }
</style>
