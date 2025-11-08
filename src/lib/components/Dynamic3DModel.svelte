<script lang="ts">
    import * as T from '@threlte/core';
    import GltfModel from '$lib/components/GltfModel.svelte';
    import { onMount, onDestroy } from 'svelte';

    // Import all known Svelte components
    import SpherePage from '../../routes/sphere/+page.svelte';
    import VaguePage from '../../routes/vague/+page.svelte';
    import TissusSimulat from '../../routes/bibi/tissus-simulat.svelte';
    import DeskPage from '../../routes/desksc/+page.svelte';
    import NissanComponent from '../../routes/Spaceship/Nissan.svelte';
    import Bibianime from '../../routes/bibi/bibanime.svelte';
    import GardenComponent from '../../routes/app/models/garden.svelte';
    import NissangameComponent from '../../routes/app/nissangame.svelte';
    import BibigameComponent from '../../routes/app/bibigame.svelte';

    export let geometry: any;

    // Map geometry types to their respective Svelte components
    const componentMap: { [key: string]: any } = {
        'sphere': SpherePage,
        'vague': VaguePage,
        'tissus': TissusSimulat,
        'desk': DeskPage,
        'nissan': NissanComponent,
        'bibi': Bibianime,
        'garden': GardenComponent,
        'nissangame': NissangameComponent,
        'bibigame': BibigameComponent,
    };

    let DynamicComponent: any = null;

    $: {
        if (geometry && geometry.model_type === 'from_file' && geometry.type) {
            DynamicComponent = componentMap[geometry.type];
            if (!DynamicComponent) {
                console.error(`No component found for type: ${geometry.type}`);
            }
        } else {
            DynamicComponent = null;
        }
    }

    // Handle component lifecycle
    onMount(() => {
        // No specific action needed here
    });

    onDestroy(() => {
        // No specific action needed here
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
