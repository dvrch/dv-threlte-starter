<script lang="ts">
    import { Canvas } from '@threlte/core'
    import Scene from '../Scene.svelte'
    import ModelUploadForm from './components/ModelUploadForm.svelte'
    import AddGeometry from './AddGeometry.svelte'
    import Tabs from './Tabs.svelte'
    import { onMount } from 'svelte'

    let activeTab = 'scene';

    function handleTabChange(event: CustomEvent) {
        activeTab = event.detail;
    }
</script>

<Tabs on:tabChange={handleTabChange} />

<div class="app-container">
    <Tabs on:tabChange={handleTabChange} />

    {#if activeTab === 'scene'}
        <div class="h-screen w-full relative">
            <Canvas>
                <Scene />
            </Canvas>
            <div class="form-container">
                <ModelUploadForm />
            </div>
        </div>
    {:else}
        <AddGeometry />
    {/if}
</div>

<style>
    .app-container {
        position: relative;
        width: 100%;
        height: 100vh;
        background: transparent;
        overflow: hidden;
    }

    .form-container {
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 100;
        pointer-events: auto;
    }
</style>

