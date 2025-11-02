<script lang="ts">
    import { T } from '@threlte/core'
    import { useGltf } from '@threlte/extras'

    const gltf = useGltf('/ghost.glb')
</script>

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
