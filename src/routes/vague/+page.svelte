<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import Vaguend from './vaguend.svelte';
</script>

<Canvas>
	<T.PerspectiveCamera makeDefault position={[0, 1, 2]}>
		<OrbitControls />
	</T.PerspectiveCamera>

	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[10, 10, 5]} />

	<Vaguend />
</Canvas>
