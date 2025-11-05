<script lang="ts">
    import { T } from '@threlte/core';
    import { Float } from '@threlte/extras';
    import GltfModel from '$lib/components/GltfModel.svelte';
    import type { PageData } from './$types';

    export let data: PageData;

</script>

{#if data.error}
    <p class="error">{data.error}</p>
{:else}
    {#each data.geometries as geometry (geometry.id)}
        <Float floatIntensity={1} floatingRange={[0, 1]}>
            {#if geometry.model_url}
                <GltfModel 
                    url={geometry.model_url} 
                    position={geometry.position}
                    rotation={geometry.rotation}
                />
            {:else if geometry.type === 'box'}
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