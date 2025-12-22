<script lang="ts">

    let { children } = $props();
    import AddGeometry from './AddGeometry.svelte';
    import { page } from '$app/stores';
    import { writable } from 'svelte/store';
    import { onMount } from 'svelte';
    import { Canvas } from '@threlte/core';
    import { T } from '@threlte/core';
    import { Grid, OrbitControls, ContactShadows } from '@threlte/extras';
    import RotatingWorld from './components/RotatingWorld.svelte';
    import Bloom from './models/bloom.svelte';

    // UI state
    let isFormHovered = $state(false);

    // Ensure normal scrolling for all routes
    onMount(() => {
        if (typeof document !== 'undefined') {
            document.body.style.overflow = '';
        }
    });
</script>

<div class="app" class:is-app-route={$page.url.pathname.startsWith('/app') || $page.url.pathname.startsWith('/vague')}>

    <main class:full-screen={$page.url.pathname.startsWith('/app') || $page.url.pathname.startsWith('/vague')}>
        <!-- 3D Canvas -->
        <div class="canvas-container">
            <Canvas renderMode="always">
                <T.Color attach="background" args={['#0a0a0a']} />
                <T.PerspectiveCamera makeDefault position={[-15, 15, 15]} fov={50}>
                    <OrbitControls enableDamping enableZoom={true} />
                </T.PerspectiveCamera>

                <T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
                <T.AmbientLight intensity={0.2} />
                <RotatingWorld>
                    <Grid position={[0, -0.001, 0]} cellColor="#ffffff" sectionColor="#ffffff" sectionThickness={0} fadeDistance={25} cellSize={2} />
                    <ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />
                    {@render children()}
                </RotatingWorld>
            </Canvas>
        </div>
        <!-- UI Controls -->
        <div class="ui-controls" onmouseenter={() => (isFormHovered = true)} onmouseleave={() => (isFormHovered = false)}>
            <div class="form-wrapper" class:is-open={isFormHovered}>
                <AddGeometry />
            </div>
        </div>
    </main>
    {#if !$page.url.pathname.startsWith('/app') && !$page.url.pathname.startsWith('/vague')}
        <footer>
            <p>© 2023 - PRESENT</p>
        </footer>
    {/if}
</div>

<style>
    .canvas-container {
        position: relative;
        width: 100%;
        height: 100vh; /* keep space for UI */
    }
    .ui-controls {
        position: fixed; /* Use fixed positioning for the controls */
        top: 80px; /* Position it lower, below the header/ribbon */
        right: 20px; /* Position it on the right side */
        z-index: 1000; /* Ensure it's above other content */
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    .form-wrapper {
        background: rgba(30, 30, 40, 0.6);
        backdrop-filter: blur(10px);
        padding: 0.5rem;
        border-radius: 8px;
        max-width: 320px;
        max-height: 50px; /* Collapsed height */
        overflow-y: auto; /* Enable vertical scroll */
        overflow-x: hidden; /* Disable horizontal scroll */
        transition: max-height 0.3s ease-out, background 0.3s ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .form-wrapper.is-open {
        max-height: 70vh; /* Expanded height (adjust as needed) */
        background: rgba(30, 30, 40, 0.8); /* More opaque when open */
    }
    @media (max-width: 600px) {
        .canvas-container {
            height: 60vh;
        }
        .ui-controls {
            left: 50%;
            right: auto;
            transform: translateX(-50%);
            top: 0.5rem;
        }
        .form-wrapper {
            width: 90%;
            left: 5%;
        }
    }
</style>
