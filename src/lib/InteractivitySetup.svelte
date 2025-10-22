<script>
    import { interactivity } from '@threlte/extras';
    import { onMount } from 'svelte';
    import { useThrelte, useFrame } from '@threlte/core'; // Correction ici
    import { useStore } from 'svelte/store';
    import { browser } from '$app/environment';

    export let orbitControls; // Accepter l'instance OrbitControls comme prop

    onMount(() => {
        if (browser) { // Exécuter cette logique uniquement côté client
            // Appeler interactivity() après que le composant soit monté et que le contexte du Canvas soit prêt
            interactivity();

            // Obtenir le store 'hovered' du système d'interactivité de Threlte
            const { hovered } = useThrelte().interactivity;
            const $hovered = useStore(hovered);

            // Configurer useFrame pour gérer l'état des OrbitControls
            const unsubscribeFrame = useFrame(() => {
                if (orbitControls) {
                    orbitControls.enabled = $hovered.length === 0;
                }
            });

            return () => {
                // Nettoyage lors de la destruction du composant
                unsubscribeFrame();
            };
        }
    });
</script>

<!-- Ce composant ne rend rien visuellement, il sert uniquement à configurer l'interactivité -->
