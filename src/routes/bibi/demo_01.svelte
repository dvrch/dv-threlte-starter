<script lang="ts">
  import { T } from '@threlte/core';

  let { position = [0, 0, 0] }: { position?: [number, number, number] } = $props();
  let { rotation = [0, 0, 0] }: { rotation?: [number, number, number] } = $props();
</script>

<T.Group {position} {rotation}>
  <T.Mesh>
    <T.BoxGeometry args={[1, 1, 1]} />
    <T.MeshBasicMaterial color={"white"} />
  </T.Mesh>
</T.Group>