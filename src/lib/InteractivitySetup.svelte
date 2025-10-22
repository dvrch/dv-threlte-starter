<script>
    import { interactivity } from '@threlte/extras';
    import { onMount } from 'svelte';

    onMount(() => {
        // Appeler interactivity() après que le composant soit monté et que le contexte du Canvas soit prêt
        interactivity();
    });
</script>

<!-- Ce composant ne rend rien visuellement, il sert uniquement à configurer l'interactivité -->