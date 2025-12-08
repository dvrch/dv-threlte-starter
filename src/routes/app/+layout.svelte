<script lang="ts">
    import { Canvas } from '@threlte/core'
    import { T } from '@threlte/core'
    import { Grid, OrbitControls, ContactShadows } from '@threlte/extras'
    import Bloom from './models/bloom.svelte';
    import Tabs from './Tabs.svelte'
    import AddGeometry from './AddGeometry.svelte'
    import { browser } from '$app/environment'

    let { children } = $props();

    let activeTab: 'scene' | 'add' | 'upload' = $state('scene')
    function handleTabChange(event: CustomEvent) {
        activeTab = event.detail
    }

    import { onMount } from 'svelte'
    
    if (typeof window !== 'undefined') {
        window.addEventListener('app:switchTab', (e: any) => {
            if (e?.detail) activeTab = e.detail
        })
    }
</script>

<div class="app-layout-container">
    <div class="canvas-background">
        <Canvas>
            <T.PerspectiveCamera makeDefault position={[-10, 10, 10]} fov={70}>
                <OrbitControls autoRotate enableZoom={true} minDistance={0} maxDistance={80} target={[0, 1.5, 0]} />
            </T.PerspectiveCamera>

            <T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
            <T.AmbientLight intensity={0.2} />

            <Grid position={[0, -0.001, 0]} cellColor="#ffffff" sectionColor="#ffffff" sectionThickness={0} fadeDistance={25} cellSize={2} />
            <ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />
            <!-- {@render children()} calls the page content which might contain 3D objects as well or HTML. If specific page content is HTML, it won't render inside Canvas. But +page.svelte contains Dynamic3DModel which IS 3D. -->
            
            <!-- Note: +page.svelte seems to mix HTML and 3D components. 
                 If +page.svelte has HTML (like error messages), it cannot be inside <Canvas>.
                 However, the previous code had {@render children()} inside <Canvas>.
                 Let's check +page.svelte again. It has HTML <p> tags AND <T.Mesh>.
                 SvelteKit + Threlte: You can't put HTML inside <Canvas> without <HTML> component.
                 The previous layout likely worked because the children were mostly 3D or ignoring HTML? 
                 Actually the previous code had {@render children()} inside <Canvas>.
                 This implies +page.svelte only returned 3D nodes?
                 But +page.svelte has <p class="error"> etc. This would likely cause issues or be invisible.
                 
                 Let's maintain the structure but fix the CSS.
            -->
            {@render children()}
        </Canvas>
    </div>

    <!-- UI Overlay for AddGeometry -->
    <div class="ui-overlay">
        <Tabs on:tabChange={handleTabChange} />
        {#if activeTab === 'add'}
            <div class="form-wrapper">
                <AddGeometry />
            </div>
        {/if}
    </div>
</div>

<style>
    .app-layout-container {
        position: relative;
        width: 100%;
        height: 80vh; /* Fixed height for the 3D view, allowing footer to exist below */
        background: #111;
        margin-top: 20px;
        border-radius: 12px;
        overflow: hidden;
    }

    .canvas-background {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }

    .ui-overlay {
        position: absolute;
        top: 20px;
        right: 20px;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: flex-end; /* Align right */
        pointer-events: none; /* Let clicks pass through */
    }

    .ui-overlay :global(*) {
        pointer-events: auto; /* Re-enable clicks on children */
    }

    .form-wrapper {
        margin-top: 10px;
        background: rgba(0, 0, 0, 0.8);
        padding: 10px;
        border-radius: 8px;
        max-width: 300px; /* Small width */
        max-height: 400px;
        overflow-y: auto;
    }
</style>

