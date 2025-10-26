<script>
  import { onMount } from 'svelte';
  import { Canvas, T } from '@threlte/core';
  import { initSn } from './demo_09.ts'; // Assurez-vous d'importer la fonction initSn
  let canvas;
  
  onMount(async () => {
    let cleanup;

    if (canvas) {
      try {
        const { renderer, animate } = await initSn(canvas); // Utilisez await ici
        function loop() {
          animate();
          requestAnimationFrame(loop);
        }
        
        loop();
        
        cleanup = () => {
          if (renderer) {
            renderer.dispose();
          }
        };
      } catch (error) {
        console.error("Erreur lors de l'initialisation de la scène:", error);
      }
    }

    return () => {
      cleanup?.();
    };
  });
</script>

<T bind:this={canvas} />