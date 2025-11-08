<script lang="ts">
    import { T } from '@threlte/core';
    import { Float } from '@threlte/extras';
    import Dynamic3DModel from '$lib/components/Dynamic3DModel.svelte';
    import type { PageData } from './$types';

    export let data: PageData;
    export let params = {};
    export let position;
    export let rotation;
    export let scale;
</script>

{#if data.error}
    <p class="error">{data.error}</p>
{:else}
    {#each data.geometries as geometry (geometry.id)}
        <Float floatIntensity={1} floatingRange={[0, 1]}>
            <Dynamic3DModel geometry={geometry} />
        </Float>
    {/each}
{/if}

<style>
    .error {
        color: red;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 1rem;
        border-radius: 8px;
    }
</style>