<script lang="ts">
	import Vaguend from './vaguend.svelte';
	import { T } from '@threlte/core';
	import { Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
</script>

<h1 style="position: absolute; top: 10px; left: 10px; z-index: 999; color: red; font-size: 2rem;">
	TEST: VAGUE PAGE LOADED
</h1>

<Canvas>
	<T.PerspectiveCamera position={[0, 1, 2]} makeDefault />
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[10, 10, 5]} />
	<OrbitControls />
	<Vaguend />
</Canvas>
