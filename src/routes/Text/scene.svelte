<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { Text3DGeometry, Float } from '@threlte/extras';
	import * as THREE from 'three';

	let { cvLines = [] }: { cvLines: string[] } = $props();

	const font =
		'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/fonts/helvetiker_bold.typeface.json';

	// Animation state
	let scrollY = $state(0);
	const lineSpacing = 1.3;
	const totalHeight = cvLines.length * lineSpacing;

	useTask((delta) => {
		scrollY += delta * 1.8; // Scroll speed
		if (scrollY > totalHeight + 15) {
			scrollY = -15; // Loop back
		}
	});

	// Pre-calculate some randomness for each line to keep it stable but organic
	const variations = $derived(
		cvLines.map(() => ({
			xOffset: (Math.random() - 0.5) * 4,
			zOffset: (Math.random() - 0.5) * 3,
			rotation: (Math.random() - 0.5) * 0.3
		}))
	);

	// Function to determine color/size based on line content
	function getLineStyle(line: string) {
		const trimmed = line.trim();
		if (trimmed.startsWith('# '))
			return { color: '#ff3e00', size: 0.7, depth: 0.2, text: trimmed.replace('# ', '') };
		if (trimmed.startsWith('## '))
			return { color: '#40b3ff', size: 0.45, depth: 0.1, text: trimmed.replace('## ', '') };
		if (trimmed.startsWith('### '))
			return { color: '#ffd700', size: 0.35, depth: 0.08, text: trimmed.replace('### ', '') };
		return {
			color: '#ffffff',
			size: 0.22,
			depth: 0.04,
			text: trimmed.startsWith('- ') ? trimmed.replace('- ', '• ') : trimmed
		};
	}
</script>

<T.PointLight position={[10, 10, 10]} intensity={2} color="#40b3ff" />
<T.PointLight position={[-10, -10, 10]} intensity={2} color="#ff3e00" />

<T.Group>
	{#each cvLines as line, i}
		{@const style = getLineStyle(line)}
		{@const v = variations[i]}
		{@const yPos = (cvLines.length - i) * lineSpacing - scrollY}

		{#if yPos > -25 && yPos < 25}
			<Float speed={1.5} rotationIntensity={0.4} floatIntensity={1}>
				<T.Group position={[v.xOffset, yPos, v.zOffset]} rotation.y={v.rotation}>
					<T.Mesh>
						<Text3DGeometry
							{font}
							text={style.text}
							size={style.size}
							depth={style.depth}
							curveSegments={5}
							bevelEnabled
							bevelSize={0.01}
							bevelThickness={0.01}
						/>
						<T.MeshStandardMaterial
							color={style.color}
							emissive={style.color}
							emissiveIntensity={0.15}
							metalness={0.9}
							roughness={0.1}
						/>
					</T.Mesh>
				</T.Group>
			</Float>
		{/if}
	{/each}
</T.Group>

<!-- Decorative elements -->
<T.Group rotation.y={scrollY * 0.05}>
	{#each Array(8) as _, i}
		<T.Mesh
			position={[Math.cos((i / 8) * Math.PI * 2) * 12, Math.sin((i / 8) * Math.PI * 2) * 12, -8]}
		>
			<T.IcosahedronGeometry args={[1.5, 0]} />
			<T.MeshStandardMaterial color="#222" wireframe />
		</T.Mesh>
	{/each}
</T.Group>
