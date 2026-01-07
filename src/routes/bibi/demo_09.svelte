<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { getLocalAssetUrl } from '$lib/utils/assets';

	// Charger le modèle animé
	const gltf = useGltf(getLocalAssetUrl('public/cloth_sim_rffdfn.glb'));

	// Animation mixer et scène Three.js native
	let mixer: THREE.AnimationMixer;
	let modelMesh: THREE.Group;

	onMount(() => {
		// Cleanup au démontage
		return () => {
			if (mixer) {
				mixer.stopAllAction();
				mixer.uncacheRoot(modelMesh);
			}
		};
	});

	// Créer un clock global pour l'animation
	const clock = new THREE.Clock();

	// Mettre à jour les animations à chaque frame
	useTask(() => {
		if (mixer) {
			mixer.update(clock.getDelta());
		}
	});

	// Configurer les animations quand le modèle est chargé
	$effect(() => {
		const gltfData = $gltf;
		if (gltfData && gltfData.scene && !mixer) {
			modelMesh = gltfData.scene;

			// Créer le mixer et jouer les animations
			mixer = new THREE.AnimationMixer(modelMesh);

			// Jouer toutes les animations trouvées
			if (gltfData.animations && gltfData.animations.length > 0) {
				gltfData.animations.forEach((clip: any) => {
					const action = mixer.clipAction(clip);
					action.play();
				});
				console.log(`Nombre d'animations trouvées: ${gltfData.animations.length}`);
			} else {
				console.warn('Aucune animation trouvée dans le modèle GLTF.');
			}
		}
	});
</script>

<T.PerspectiveCamera makeDefault position={[0, 1.5, 5.2]} fov={75} />
<T.AmbientLight color="#555555" intensity={10} />
<T.PointLight position={[0, 4, 4]} intensity={1} />

{#if $gltf && $gltf.scene}
	<T is={$gltf.scene} scale={1} />
{/if}
