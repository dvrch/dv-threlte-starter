<script lang="ts">
  import { onMount } from 'svelte';
  import { initSn } from './demo_09.js';
  
  let { data, params } = $props();
  let canvas: HTMLCanvasElement;
  let animationId: number;
  
  onMount(() => {
    let cleanup: (() => void) | undefined;
  
    if (canvas) {
      initSn(canvas).then(({ renderer, animate }) => {
        function loop() {
          animate();
          animationId = requestAnimationFrame(loop);
        }
        
        loop();
        
        cleanup = () => {
          cancelAnimationFrame(animationId);
          renderer.dispose();
        };
      }).catch(error => {
        console.error("Erreur lors de l'initialisation de la scène:", error);
      });
    }
  
    return () => {
      cleanup?.();
    };
  });
  </script>
  
  <canvas bind:this={canvas} id="canvas"></canvas>
  
  <style>
  canvas {
    width: 100%;
    height: 100vh;
  }
  </style>
  
  
  
  <!-- <script lang="ts">
import { Canvas } from '@threlte/core';
import Demo_09 from './demo_09.svelte'; // Assurez-vous que le chemin est correct
</script>

<Canvas>
  <Demo_09 />
</Canvas> -->
