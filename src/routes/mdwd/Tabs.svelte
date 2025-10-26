<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  let activeTab = 'scene';

  function setTab(tab: string) {
    activeTab = tab;
    dispatch('tabChange', tab);
  }
</script>

<div class="tabs">
  <button class:active={activeTab === 'scene'} on:click={() => setTab('scene')}>Scene</button>
  <button class:active={activeTab === 'add'} on:click={() => setTab('add')}>Add Geometry</button>
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
