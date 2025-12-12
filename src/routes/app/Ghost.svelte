<script lang="ts">
    import { T } from '@threlte/core'
    import { useGltf } from '@threlte/extras'
    import { getCloudinaryAssetUrl, dracoGltfLoader } from '$lib/utils/cloudinaryAssets';

    const gltf = useGltf(getCloudinaryAssetUrl('/ghost.glb'), { loader: dracoGltfLoader })</script>

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
