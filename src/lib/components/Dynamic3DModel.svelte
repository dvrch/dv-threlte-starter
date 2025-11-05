<script lang="ts">
    import { T } from '@threlte/core';
    import GltfModel from '$lib/components/GltfModel.svelte';
    import { onMount, onDestroy } from 'svelte';

    export let geometry: any;

    let DynamicComponent: any = null;

    $: if (geometry && geometry.model_type === 'from_file' && geometry.model_url) {
        // Dynamically import the Svelte component
        import(/* @vite-ignore */ geometry.model_url)
            .then(module => {
                DynamicComponent = module.default;
            })
            .catch(error => {
                console.error(`Failed to load dynamic component from ${geometry.model_url}:`, error);
                DynamicComponent = null; // Reset on error
            });
    } else {
        DynamicComponent = null; // Reset if not from_file or no url
    }

    // Handle component lifecycle
    onMount(() => {
        // No specific action needed here as componentInstance is managed by {#if DynamicComponent}
    });

    onDestroy(() => {
        // No specific action needed here as componentInstance is managed by {#if DynamicComponent}
    });
</script>

{#if geometry.model_type === 'from_file' && DynamicComponent}
    <!-- Render the dynamically loaded Svelte component -->
    <T.Group
        position={[geometry.position.x, geometry.position.y, geometry.position.z]}
        rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
        scale={geometry.scale || 1}
    >
        <svelte:component this={DynamicComponent} />
    </T.Group>
{:else if geometry.model_url}
    <!-- Render a GLTF model if model_url is present and not from_file -->
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
{:else if geometry.type === 'sphere'}
    <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]}
            rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
        <T.SphereGeometry />
        <T.MeshStandardMaterial color={geometry.color} />
    </T.Mesh>
{:else}
    <!-- Fallback for unhandled types -->
    <T.Mesh position={[geometry.position.x, geometry.position.y, geometry.position.z]}
            rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]} scale={0.5}>
        <T.BoxGeometry />
        <T.MeshStandardMaterial color="purple" />
    </T.Mesh>
{/if}
