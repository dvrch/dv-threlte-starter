<script>
    import { interactivity } from '@threlte/extras';
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';

    onMount(() => {
        if (browser) {
            interactivity();
        }
    });
</script>

<!-- Ce composant ne rend rien visuellement, il sert uniquement à configurer l'interactivité -->
