<script lang="ts">
	import { T } from '@threlte/core';
	import { Environment, OrbitControls } from '@threlte/extras';
	import { Effect, Bloom, SMAA } from '@threlte/postprocessing';
	import Stars from '$lib/components/Stars.svelte';
	import Spaceship from '$lib/components/models/spaceship.svelte';
	import Nissan from '$lib/components/.Nissan';

	let spaceShipRef: any = null;
</script>

<T.PerspectiveCamera makeDefault position={[-5, 6, 10]} fov={25}>
	<OrbitControls enableDamping target={[0, 0, 0]} />
</T.PerspectiveCamera>

<Environment
	path="/textures/kloppenheim_05_1k.hdr"
	isBackground
/>

<Effect>
	<Bloom
		intensity={0.8}
		luminanceThreshold={0}
		luminanceSmoothing={0}
		mipmapBlur
		height={512}
		width={512}
	/>
	<SMAA />
</Effect>

<T.DirectionalLight intensity={1.8} position={[0, 10, 0]} castShadow shadow.bias={-0.0001} />

<Spaceship ref={spaceShipRef} />

<Stars />

<Nissan ref={spaceShipRef} />
