<script lang="ts">
    let { children } = $props();
    import AddGeometry from './AddGeometry.svelte';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { Canvas } from '@threlte/core';
    import { T } from '@threlte/core';
    import { Grid, OrbitControls, ContactShadows } from '@threlte/extras';
    import RotatingWorld from './components/RotatingWorld.svelte';
    import Bloom from './models/bloom.svelte';

    // UI state
    let isFormHovered = $state(false);
    let isInteracting = $state(false);
    let isDraggingGlobal = $state(false);

    // Auto-rotation handling
    let interactionTimeout: any;

    const startInteraction = () => {
        isInteracting = true;
        if (interactionTimeout) clearTimeout(interactionTimeout);
    };

    const stopInteraction = () => {
        // Delay resuming rotation for better feel
        interactionTimeout = setTimeout(() => {
            isInteracting = false;
        }, 3000);
    };

    // Global drag & drop for direct upload
    const handleGlobalDragOver = (e: DragEvent) => {
        if (!$page.url.pathname.startsWith('/app')) return;
        e.preventDefault();
        isDraggingGlobal = true;
    };

    const handleGlobalDragLeave = (e: DragEvent) => {
        // Only trigger if we actually left the window
        if (e.relatedTarget === null) {
            isDraggingGlobal = false;
        }
    };

    const handleGlobalDrop = (e: DragEvent) => {
        if (!$page.url.pathname.startsWith('/app')) return;
        e.preventDefault();
        isDraggingGlobal = false;
        
        if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            const ext = file.name.split('.').pop()?.toLowerCase();
            if (ext === 'glb' || ext === 'gltf') {
                window.dispatchEvent(new CustomEvent('directSceneUpload', { detail: { file } }));
            }
        }
    };

    let isCameraLocked = $state(false);

    onMount(() => {
        if (typeof document !== 'undefined') {
            document.body.style.overflow = '';
        }
        
        const handleLock = () => (isCameraLocked = true);
        const handleUnlock = () => (isCameraLocked = false);
        window.addEventListener('lockCamera', handleLock);
        window.addEventListener('unlockCamera', handleUnlock);

        return () => {
            window.removeEventListener('lockCamera', handleLock);
            window.removeEventListener('unlockCamera', handleUnlock);
        };
    });
</script>

<div 
    class="app" 
    class:is-app-route={$page.url.pathname.startsWith('/app') || $page.url.pathname.startsWith('/vague')}
    ondragover={handleGlobalDragOver}
    ondragleave={handleGlobalDragLeave}
    ondrop={handleGlobalDrop}
    role="presentation"
>
    {#if isDraggingGlobal}
        <div class="drop-overlay">
            <div class="drop-message">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                <span>Déposez votre modèle 3D ici pour l'ajouter instantanément</span>
            </div>
        </div>
    {/if}

    <main class:full-screen={$page.url.pathname.startsWith('/app') || $page.url.pathname.startsWith('/vague')}>
        <div class="canvas-container">
            <Canvas renderMode="always">
                <T.Color attach="background" args={['#12121e']} />
                <T.PerspectiveCamera makeDefault position={[-15, 15, 15]} fov={50}>
                    <OrbitControls 
                        enabled={!isCameraLocked}
                        enableDamping 
                        enableZoom={true}
                        onstart={startInteraction}
                        onend={stopInteraction}
                        autoRotate={!isInteracting && !isCameraLocked}
                        autoRotateSpeed={0.5}
                    />
                </T.PerspectiveCamera>

                <T.DirectionalLight intensity={0.8} position={[5, 10, 0]} />
                <T.AmbientLight intensity={0.2} />
                
                <RotatingWorld isPaused={isInteracting}>
                    <Grid position={[0, -0.001, 0]} cellColor="#ffffff" sectionColor="#ffffff" sectionThickness={0} fadeDistance={25} cellSize={2} />
                    <ContactShadows scale={10} blur={2} far={2.5} opacity={0.5} />
                    {@render children()}
                </RotatingWorld>
            </Canvas>
        </div>

        <div 
            class="ui-controls" 
            onmouseenter={() => (isFormHovered = true)} 
            onmouseleave={() => (isFormHovered = false)}
            role="region"
            aria-label="Geometry controls"
        >
            <div class="form-wrapper" class:is-open={isFormHovered}>
                <AddGeometry />
            </div>
        </div>
    </main>
</div>

<style>
    .canvas-container {
        position: relative;
        width: 100%;
        height: 100vh;
    }
    .ui-controls {
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }
    .form-wrapper {
        background: rgba(30, 30, 40, 0.4);
        backdrop-filter: blur(8px);
        padding: 0.5rem;
        border-radius: 8px;
        width: 320px;
        max-height: 42px; /* Ultra-compact when closed */
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        cursor: pointer;
    }
    .form-wrapper.is-open {
        max-height: 85vh;
        background: rgba(20, 20, 25, 0.95);
        border-color: rgba(77, 182, 172, 0.3);
        box-shadow: 0 12px 40px rgba(0,0,0,0.6);
        overflow-y: auto;
    }

    .drop-overlay {
        position: fixed;
        inset: 0;
        background: rgba(77, 182, 172, 0.2);
        backdrop-filter: blur(4px);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 4px dashed #4db6ac;
        margin: 20px;
        border-radius: 20px;
        pointer-events: none;
    }
    .drop-message {
        background: #1e1e28;
        padding: 2rem;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        color: #4db6ac;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    @media (max-width: 600px) {
        .ui-controls {
            left: 50%;
            right: auto;
            transform: translateX(-50%);
            top: 0.5rem;
        }
    }
</style>
