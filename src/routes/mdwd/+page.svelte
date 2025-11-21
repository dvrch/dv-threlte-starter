<script lang="ts">
  export const data = undefined;
  export const params = {};

  import { Canvas } from '@threlte/core'
  import Scene from './Markdown.svelte'
  import AddGeometry from './word.svelte'
  import Tabs from './Tabs.svelte'

  let activeTab = 'scene';

  function handleTabChange(event: CustomEvent) {
    activeTab = event.detail;
    // Force Svelte to re-render the component
    activeTab = '';
    setTimeout(() => {
      activeTab = event.detail;
    }, 0);
  }
</script>

<Tabs on:tabChange={handleTabChange} />

{#if activeTab === 'scene'}
<div class="app-container" style="overflow: hidden; width: 92vw; height: 92vh; margin: 4vw 4vh;">
  <Canvas>
    <Scene />
  </Canvas>
  <div class="form-container">
    <AddGeometry />
  </div>
</div>
{:else}
    <AddGeometry />
{/if}

<style>
  .app-container {
    position: relative;
    width: 95vw; /* Ajusté pour occuper 95% de la largeur de la fenêtre */
    height: 95vh; /* Ajusté pour occuper 95% de la hauteur de la fenêtre */
    background: transparent;
    overflow: hidden; /* Assurez-vous que le débordement est caché */
    max-width: 95%; /* Ajusté pour occuper 95% de la largeur de la fenêtre */
    max-height: 95%; /* Ajusté pour occuper 95% de la hauteur de la fenêtre */
  }

  .form-container {
    position: fixed; /* Positionner le formulaire par rapport à la fenêtre */
    top: 100px; /* Ajusté pour s'assurer qu'il est visible */
    right: 10px; /* Ajusté pour s'assurer qu'il est visible */
    pointer-events: auto; /* Permettre les interactions avec le formulaire */
    z-index: 1; /* Assurez-vous que le formulaire est au-dessus de la scène */
    opacity: 0.9; /* Rendre le formulaire semi-transparent */
    background: transparent;
  }
</style>
