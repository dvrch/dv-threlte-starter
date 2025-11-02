<script lang="ts">
    import { onMount } from 'svelte';
    import { T } from '@threlte/core';
    import { Float } from '@threlte/extras';
    import ModelUploadForm from '$lib/components/ModelUploadForm.svelte';
    import AddGeometry from './AddGeometry.svelte';
    import Tabs from './Tabs.svelte';
    import Notification from '$lib/components/Notification.svelte';
    import { notification } from '$lib/stores/notification';
    import type { PageData } from './$types';

    export let data: PageData;
</script>

    let geometries = [];

    const loadGeometries = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/geometries/');
            if (!response.ok) {
                throw new Error('Failed to fetch geometries');
            }
            const responseData = await response.json();
            // DRF paginates the results, so we need to get the `results` array
            geometries = responseData.results || responseData;
            console.log('Loaded geometries:', geometries);
        } catch (error) {
            console.error('Error loading geometries:', error);
            notification.show('Failed to load geometries', 'error');
        }
    };

    onMount(loadGeometries);

    let activeTab = 'scene';

    function handleTabChange(event: CustomEvent) {
        activeTab = event.detail;
    }

    onMount(() => {
        window.onerror = (msg, url, lineNo, columnNo, error) => {
            notification.show(error?.message || String(msg), 'error');
            return false;
        };

        const handleModelAdded = () => {
            loadGeometries();
        };
        window.addEventListener('modelAdded', handleModelAdded);

        return () => {
            window.removeEventListener('modelAdded', handleModelAdded);
        };
    });
</script>

{#each geometries as geometry (geometry.id)}
    <Float floatIntensity={1} floatingRange={[0, 1]}>
        {#if geometry.type === 'box'}
            <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
            rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
                <T.BoxGeometry />
                <T.MeshStandardMaterial color={geometry.color} />
            </T.Mesh>
        {:else if geometry.type === 'torus'}
            <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
            rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
                <T.TorusKnotGeometry args={[0.5, 0.15, 100, 12, 2, 3]} />
                <T.MeshStandardMaterial color={geometry.color} />
            </T.Mesh>
        {:else if geometry.type === 'icosahedron'}
            <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]} 
            rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
                <T.IcosahedronGeometry />
                <T.MeshStandardMaterial color={geometry.color} />
            </T.Mesh>
        {/if}
        <!-- Add other geometry types here -->
    </Float>
{/each}

<div class="ui-overlay">
    <h1>TEST UI OVERLAY</h1>
</div>

<style>
    .ui-overlay {
        position: absolute;
        top: 60px;
        right: 20px;
        z-index: 100;
    }

    .controls-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .upload-form-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .full-geometry-view {
        padding: 20px;
        height: calc(100vh - 120px);
        overflow-y: auto;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
</style>