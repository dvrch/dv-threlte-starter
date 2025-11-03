<script lang="ts">
    import { Canvas, T } from '@threlte/core'
    import { Grid, OrbitControls, ContactShadows } from '@threlte/extras'
    import Bloom from '$lib/components/bloom.svelte';
    import Tabs from './Tabs.svelte'
    import AddGeometry from './AddGeometry.svelte'
    import ModelUploadForm from '$lib/components/ModelUploadForm.svelte'
    export let data;
    // params n'est pas utilisé, mais requis par SvelteKit pour la compatibilité
    export let params = {};

    let activeTab: 'scene' | 'add' | 'upload' = 'scene'
    function handleTabChange(event: CustomEvent) {
        activeTab = event.detail
    }
</script>

<div style="position: relative; width: 100%; height: 100vh;">
    <Canvas>
        <T.PerspectiveCamera makeDefault position={[-10, 10, 10]} fov={70}>
            <OrbitControls autoRotate enableZoom={true} minDistance={0} maxDistance={80} target={[0, 1.5, 0]} />
        </T.PerspectiveCamera>

        <T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
        <T.AmbientLight intensity={0.2} />

        <Grid position={[0, -0.001, 0]} cellColor="#ffffff" sectionColor="#ffffff" sectionThickness={0} fadeDistance={25} cellSize={2} />
        <ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />
        <Bloom />

        <slot />
    </Canvas>
    <div class="ui-overlay-root" style="position:absolute; top: 60px; right: 20px; z-index: 2000; display:flex; flex-direction:column; gap:12px;">
        <Tabs on:tabChange={handleTabChange} />
        {#if activeTab === 'scene'}
            <div class="upload-form-container" style="background: rgba(255,255,255,0.9); border-radius:8px; padding:12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <ModelUploadForm />
            </div>
        {:else if activeTab === 'add'}
            <AddGeometry />
        {:else if activeTab === 'upload'}
            <div class="upload-form-container" style="background: rgba(255,255,255,0.9); border-radius:8px; padding:12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <ModelUploadForm />
            </div>
        {/if}
    </div>
</div>