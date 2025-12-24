<script lang="ts">
    import { T, useThrelte } from '@threlte/core';
    import { OrbitControls } from '@threlte/extras';

    const { size } = useThrelte();

    let {
        isCameraLocked,
        startInteraction,
        stopInteraction,
        isInteracting
    }: {
        isCameraLocked: boolean;
        startInteraction: () => void;
        stopInteraction: () => void;
        isInteracting: boolean;
    } = $props();
</script>

<T.PerspectiveCamera makeDefault position={[-15, 15, 15]} fov={50} aspect={$size.aspect}>
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
