<script lang="ts">
    import { T } from '@threlte/core'
    import { useGltf } from '@threlte/extras'
    import { getCloudinaryAssetUrl } from '$lib/utils/cloudinaryAssets';
    import { dracoLoader } from '$lib/utils/draco';

    const gltf = useGltf(getCloudinaryAssetUrl('/ghost.glb'), { dracoLoader })
<T.Group>
    {#if $gltf}
        <T.Primitive 
            object={$gltf.scene} 
            position={[0, 0, 0]}
            scale={1}
            rotation={[0, 0, 0]}
        />
    {/if}
</T.Group>
