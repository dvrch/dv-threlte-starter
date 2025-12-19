<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import * as THREE from 'three';

	// Props
	let {
		position = [0, 0, 0],
		rotation = [0, 0, 0],
		scale = 1
	}: {
		position?: [number, number, number];
		rotation?: [number, number, number];
		scale?: number | [number, number, number];
	} = $props();

	// Logique pour créer et animer la géométrie des vagues
	function computeGeometry(): THREE.BufferGeometry {
		const space = 4,
			nb = 100,
			amp = 0.1,
			pi2 = Math.PI * 2;
		const geometry = new THREE.BufferGeometry();
		const positions = new Float32Array(nb * nb * 3);
		const colors = new Float32Array(nb * nb * 3);
		let k = 0;

		for (let i = 0; i < nb; i++) {
			for (let j = 0; j < nb; j++) {
				const x = i * (space / nb) - space / 2;
				const z = j * (space / nb) - space / 2;
				const y = amp * (Math.cos(x * pi2) + Math.sin(z * pi2));
				positions[3 * k + 0] = x;
				positions[3 * k + 1] = y;
				positions[3 * k + 2] = z;
				const intensity = y / amp / 2 + 0.3;
				colors[3 * k + 0] = (j / nb) * intensity;
				colors[3 * k + 1] = 0;
				colors[3 * k + 2] = (i / nb) * intensity;
				k++;
			}
		}
		geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
		geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
		geometry.computeBoundingBox();
		return geometry;
	}

	function animeGeometry(geometry: THREE.BufferGeometry, progress: number): void {
		const space = 4,
			nb = 100,
			amp = 0.1,
			pi2 = Math.PI * 2;
		const phase = progress;
		const fre = 0.8 + Math.cos(progress) / 2;
		let k = 0;
		for (let i = 0; i < nb; i++) {
			for (let j = 0; j < nb; j++) {
				const x = i * (space / nb) - space / 2;
				const z = j * (space / nb) - space / 2;
				const y = amp * (Math.cos(x * pi2 * fre + phase) + Math.sin(z * pi2 * fre + phase));
				if (geometry.attributes.position) {
					geometry.attributes.position.setY(k, y);
				}
				const intensity = y / amp / 2 + 0.3;
				if (geometry.attributes.color) {
					geometry.attributes.color.setX(k, (j / nb) * intensity);
					geometry.attributes.color.setZ(k, (i / nb) * intensity);
				}
				k++;
			}
		}
		if (geometry.attributes.position) geometry.attributes.position.needsUpdate = true;
		if (geometry.attributes.color) geometry.attributes.color.needsUpdate = true;
	}

	// Créer la géométrie une seule fois
	const geometry = computeGeometry();

	// Créer un clock pour l'animation
	const clock = new THREE.Clock();
	let t = $state(0);

	// Utiliser la boucle de rendu de Threlte pour l'animation
	useTask(() => {
		t += clock.getDelta();
		animeGeometry(geometry, t);
	});
</script>

<!-- Le composant affiche simplement les points animés -->
<T.Points {geometry} rotation.y={0.1 * t} rotation.z={0.1 * t}>
	<T.PointsMaterial size={0.015} vertexColors={true} />
</T.Points>
