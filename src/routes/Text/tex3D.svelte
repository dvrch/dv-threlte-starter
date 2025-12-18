<script lang="ts">
	import { T } from '@threlte/core';
	import { Text3DGeometry } from '@threlte/extras';

	const font =
		'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/fonts/helvetiker_bold.typeface.json';

	const size = 1;
	const depth = size / 2; // profondeur = moitié de la hauteur visuelle
</script>

<T.Group position={[0, 0, 3]}>
	<T.Mesh>
		<Text3DGeometry {font} text="Hello 3D" {size} {depth} curveSegments={12} />
		<T.MeshStandardMaterial color="red" />
	</T.Mesh>
</T.Group>

<T.Mesh position={[-3, 0.5, 3]}>
	<T.SphereGeometry args={[0.5, 32, 32]} />
	<T.MeshStandardMaterial color="blue" />
</T.Mesh>
