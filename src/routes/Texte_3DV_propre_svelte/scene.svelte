<script lang="ts">
	import { Canvas } from '@threlte/core';
	import * as T from '@threlte/extras';
	import { degToRad } from 'three/src/math/MathUtils.js';
</script>

<Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
	<T.AmbientLight intensity={0.5} />
	<T.DirectionalLight position={[5, 5, 5]} intensity={1} />

	<T.Group position={[0, 0, 0]} rotation={[degToRad(0), degToRad(0), 0]}>
		<T.Mesh>
			<T.Text3DGeometry
				font="/fonts/InterExtraBold.json"
				text="Hello 3D"
				size={1}
				height={0.3}
				depth={0.5}
			/>
			<T.MeshStandardMaterial color="red" />
		</T.Mesh>
	</T.Group>
</Canvas>
