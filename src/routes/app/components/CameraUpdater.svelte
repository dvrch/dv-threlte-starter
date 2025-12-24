<script lang="ts">
    import { useThrelte } from '@threlte/core';
    import { untrack } from 'svelte';

    const { camera, size } = useThrelte();

    $effect(() => {
        const cam = untrack(() => $camera);
        if (cam && $size) {
            (cam as any).aspect = $size.width / $size.height;
            (cam as any).updateProjectionMatrix();
        }
    });
</script>
