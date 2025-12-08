<script lang="ts">

    let { children } = $props();
    import AddGeometry from './AddGeometry.svelte';
    import { page } from '$app/stores';
    import { writable } from 'svelte/store';
    import { onMount } from 'svelte';
    import { Canvas } from '@threlte/core';
    import { T } from '@threlte/core';
    import { Grid, OrbitControls, ContactShadows } from '@threlte/extras';
    import Bloom from './models/bloom.svelte';

    // UI state
    const showForm = writable(false);
    const toggleForm = () => showForm.update(v => !v);

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
            <Canvas>
                <T.PerspectiveCamera makeDefault position={[-10, 10, 10]} fov={70} />
                <OrbitControls autoRotate enableZoom={true} minDistance={0} maxDistance={80} target={[0, 1.5, 0]} />
                <T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
                <T.AmbientLight intensity={0.2} />
                <Grid position={[0, -0.001, 0]} cellColor="#ffffff" sectionColor="#ffffff" sectionThickness={0} fadeDistance={25} cellSize={2} />
                <ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />
                {@render children()}
            </Canvas>
        </div>
        <!-- UI Controls -->
        <div class="ui-controls">
            <button class="toggle-form" onclick={toggleForm} aria-label="Toggle Add Geometry Form">
                {#if $showForm}✖ Close Form{:else}+ Add Geometry{/if}
            </button>
            {#if $showForm}
                <div class="form-wrapper">
                    <AddGeometry />
                </div>
            {/if}
        </div>
    </main>
    {#if !$page.url.pathname.startsWith('/app') && !$page.url.pathname.startsWith('/vague')}
        <footer>
            <p>© 2023 - PRESENT</p>
        </footer>
    {/if}
</div>

<style>
    :global(html) {
        background: #121212; /* dark background */
        color: #e0e0e0;   /* light text */
        font-family: 'Inter', sans-serif;
    }
    .canvas-container {
        position: relative;
        width: 100%;
        height: 100vh; /* keep space for UI */
    }
    .ui-controls {
        position: absolute;
        top: 1rem;
        right: 1rem;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    .toggle-form {
        background: #4db6ac;
        color: #000;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        margin-bottom: 0.5rem;
    }
    .form-wrapper {
        background: rgba(30, 30, 40, 0.85);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 8px;
        max-width: 320px;
        max-height: 70vh;
        overflow-y: auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
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
