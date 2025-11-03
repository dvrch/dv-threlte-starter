<script lang="ts">
    import { Canvas, T } from '@threlte/core'
    import { Grid, OrbitControls, ContactShadows } from '@threlte/extras'
    import Bloom from '$lib/components/bloom.svelte';
    export let data;
    // params n'est pas utilisé, mais requis par SvelteKit pour la compatibilité
    export let params = {};
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
</div>