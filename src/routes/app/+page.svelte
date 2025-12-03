<script lang="ts">
    import { T } from '@threlte/core';
    import { Float } from '@threlte/extras';
    import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
    import { browser } from '$app/environment';
    import { onMount } from 'svelte';
    import { PUBLIC_API_URL } from '$env/static/public';

    let geometries = $state([]);
    let loading = $state(true);
    let error = $state<string | null>(null);

    onMount(async () => {
        try {
            const apiUrl = PUBLIC_API_URL
                ? `${PUBLIC_API_URL}/api/geometries/`
                : '/api/geometries/';

            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            geometries = data.results || [];
            console.log('Loaded geometries:', geometries.length);
        } catch (e) {
            error = (e as Error).message;
            console.error('Error loading geometries:', e);
        } finally {
            loading = false;
        }
    });
</script>

{#if error}
    <p class="error">Erreur: {error}</p>
{:else if loading}
    <p class="loading">Chargement des géométries...</p>
{:else if geometries.length === 0}
    <p class="empty">Aucune géométrie trouvée</p>
{:else}
    <T.Canvas>
        <T.PerspectiveCamera
            makeDefault
            position={[5, 5, 5]}
            on:create={({ ref }) => {
                ref.lookAt(0, 0, 0);
            }}
        />
        <T.AmbientLight intensity={0.5} />
        <T.DirectionalLight position={[10, 10, 5]} />

        {#each geometries as geometry (geometry.id)}
            {#if browser}
                <Float floatIntensity={1} floatingRange={[0, 1]}>
                    <Dynamic3DModel {geometry} />
                </Float>
            {:else}
                <!-- Fallback for SSR -->
                <Dynamic3DModel {geometry} />
            {/if}
        {/each}
    </T.Canvas>
{/if}

<style>
    .error, .loading, .empty {
        color: white;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 8px;
        z-index: 100;
    }
</style>
