<script lang="ts">
    import { Canvas } from '@threlte/core'
    import Scene from '../Scene.svelte'
    import ModelUploadForm from './components/ModelUploadForm.svelte'
    import AddGeometry from './AddGeometry.svelte'
    import Tabs from './Tabs.svelte'
    import Notification from '$lib/components/Notification.svelte'
    import { notification } from '$lib/stores/notification'
    import { onMount } from 'svelte'
    import type { PageData } from './$types'

    export let data: PageData

    let activeTab = 'scene';

    function handleTabChange(event: CustomEvent) {
        activeTab = event.detail;
    }

    onMount(() => {
        window.onerror = (msg, url, lineNo, columnNo, error) => {
            notification.show(error?.message || String(msg), 'error');
            return false;
        };
    });
</script>

<Tabs on:tabChange={handleTabChange} />

<div class="app-container">
    <Notification />
    <Tabs on:tabChange={handleTabChange} />

    {#if activeTab === 'scene'}
        <div class="scene-container">
            <Canvas>
                <Scene />
            </Canvas>
            <div class="controls-container">
                <div class="upload-form-container">
                    <ModelUploadForm />
                </div>
                <div class="geometry-controls">
                    <AddGeometry />
                </div>
            </div>
        </div>
    {:else}
        <div class="full-geometry-view">
            <AddGeometry />
        </div>
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

    .scene-container {
        position: relative;
        width: 100%;
        height: calc(100vh - 50px);
    }

    .controls-container {
        position: fixed;
        top: 60px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;
        z-index: 100;
        pointer-events: none;
    }

    .upload-form-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 15px;
        pointer-events: auto;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .geometry-controls {
        pointer-events: auto;
    }

    .full-geometry-view {
        padding: 20px;
        height: calc(100vh - 50px);
        overflow-y: auto;
    }
</style>

