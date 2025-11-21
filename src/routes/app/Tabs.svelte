<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  let activeTab = $state('scene');

  function setTab(tab: string) {
    activeTab = tab;
    dispatch('tabChange', tab);
  }
</script>

<div class="tabs">
  <button class:active={activeTab === 'scene'} onclick={() => setTab('scene')}>Scene</button>
  <button class:active={activeTab === 'add'} onclick={() => setTab('add')}>Add Geometry</button>
  <button class:active={activeTab === 'upload'} onclick={() => setTab('upload')}>Upload 3D</button>
</div>

<style>
  .tabs {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
  }
  button {
    padding: 0.5rem 1rem;
    border: none;
    background-color: #f0f0f0;
    cursor: pointer;
  }
  button.active {
    background-color: #007bff;
    color: white;
  }
</style>
