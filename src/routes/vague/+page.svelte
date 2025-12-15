<script lang="ts">
	import Vaguend from './vaguend.svelte';
	import { T } from '@threlte/core';
	import { Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
</script>

<Canvas>
	<T.PerspectiveCamera position={[0, 1, 2]} makeDefault />
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[10, 10, 5]} />
	<OrbitControls />
	<Vaguend />
</Canvas>
