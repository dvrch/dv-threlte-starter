<script>
    import { interactivity } from '@threlte/extras';
    import { onMount } from 'svelte';
    import { useThrelte, useTask } from '@threlte/core';
    // import { useStore } from 'svelte/store'; // Supprimer cette importation
    import { browser } from '$app/environment';

    export let orbitControls; // Accepter l'instance OrbitControls comme prop

    let hovered; // Déclarer hovered comme une variable réactive pour utiliser la syntaxe $hovered

    onMount(() => {
        if (browser) { // Exécuter cette logique uniquement côté client
            // Appeler interactivity() après que le composant soit monté et que le contexte du Canvas soit prêt
            interactivity();

            // Obtenir le store 'hovered' du système d'interactivité de Threlte
            const threlte = useThrelte();
            hovered = threlte.interactivity.hovered; // Assigner le store à la variable réactive

            // Configurer useTask pour gérer l'état des OrbitControls
            const unsubscribeTask = useTask(() => {
                if (orbitControls) {
                    orbitControls.enabled = $hovered.length === 0; // Utiliser la syntaxe $hovered
                }
            });

            return () => {
                // Nettoyage lors de la destruction du composant
                unsubscribeTask();
            };
        }
    });
</script>

<!-- Ce composant ne rend rien visuellement, il sert uniquement à configurer l'interactivité -->