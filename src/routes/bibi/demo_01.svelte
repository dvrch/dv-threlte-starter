<script lang="ts">
  import { T } from '@threlte/core';

  export let position: [number, number, number] = [0, 0, 0];
  export let rotation: [number, number, number] = [0, 0, 0];
</script>

<T.Group {position} {rotation}>
  <T.Mesh>
    <T.BoxGeometry args={[1, 1, 1]} />
    <T.MeshBasicMaterial color={"white"} />
  </T.Mesh>
</T.Group>