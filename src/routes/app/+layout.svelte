<script lang="ts">
    import { Canvas, T } from '@threlte/core'
    import { Grid, OrbitControls, ContactShadows } from '@threlte/extras'
    import Bloom from '$lib/components/bloom.svelte';
    import Tabs from './Tabs.svelte'
    import AddGeometry from './AddGeometry.svelte'
    // aucune donnée de layout utilisée ici

	let { children } = $props();

    let activeTab: 'scene' | 'add' | 'upload' = $state('scene')
    function handleTabChange(event: CustomEvent) {
        activeTab = event.detail
    }

    import { onMount } from 'svelte'
    onMount(() => {
        const handleSwitch = (e: CustomEvent) => {
            activeTab = (e.detail ?? 'scene') as any
        }
        window.addEventListener('app:switchTab', handleSwitch as EventListener)
        return () => window.removeEventListener('app:switchTab', handleSwitch as EventListener)
    })

    if (typeof window !== 'undefined') {
        window.addEventListener('app:switchTab', (e: any) => {
            if (e?.detail) activeTab = e.detail
        })
    }
</script>

<div style="position: relative; width: 100%; height: 100vh;">
    <!-- enable pointer events so OrbitControls and mouse interaction work -->
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: auto;">
        <Canvas>
            <T.PerspectiveCamera makeDefault position={[-10, 10, 10]} fov={70}>
                <OrbitControls autoRotate enableZoom={true} minDistance={0} maxDistance={80} target={[0, 1.5, 0]} />
            </T.PerspectiveCamera>

            <T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
            <T.AmbientLight intensity={0.2} />

            <Grid position={[0, -0.001, 0]} cellColor="#ffffff" sectionColor="#ffffff" sectionThickness={0} fadeDistance={25} cellSize={2} />
            <ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />
            {#if browser}
                <Bloom />
            {/if}

            {@render children()}
        </Canvas>
    </div>
    <div class="ui-overlay-root" style="position:absolute; top: 60px; right: 20px; z-index: 2000; display:flex; flex-direction:column; gap:12px; pointer-events: auto;">
        <Tabs on:tabChange={handleTabChange} />
        {#if activeTab === 'add'}
            <AddGeometry />
        {/if}
    </div>
</div>