<script lang="ts">
	import { writable } from 'svelte/store';
	import { T, Canvas } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { onMount } from 'svelte';
	import { navigate } from 'svelte-routing';
	import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry';
	import { assets } from '$lib/services/assets';
	import { FontLoader, Font } from 'three/examples/jsm/loaders/FontLoader.js';

	const clock = new THREE.Clock();
	const model = writable<THREE.Object3D | null>(null);
	let mixer: THREE.AnimationMixer;
	let font: Font | null = null; // Now correctly typed with 'Font'

	onMount(async () => {
		try {
			const gltf = await new GLTFLoader().loadAsync(
				'https://res.cloudinary.com/drcok7moc/raw/upload/v1765419051/dv-threlte/models/jaaezicvyjlywsw6lgwu.glb'
			);
			const texture = await new THREE.TextureLoader().loadAsync('/public/zaki.png');

			const mesh = gltf.scene.children[0] as THREE.Mesh;
			if (mesh.material) {
				mesh.material = new THREE.MeshPhongMaterial({ map: texture, shininess: 10 });
			}

			mixer = new THREE.AnimationMixer(gltf.scene);
			gltf.animations.forEach((clip) => mixer.clipAction(clip).play());

			animate();

			// Charger la police
			const loader = new FontLoader();
			font = await loader.loadAsync(assets.getUrl('/fonts/font.json'));

			// Vérifiez si la police est chargée avant de créer le maillage de texte
			if (font) {
				model.set(gltf.scene); // Déplacez cette ligne ici si nécessaire
			}
		} catch (error) {
			console.error('Erreur lors du chargement du modèle ou de la texture:', error);
		}
	});

	function animate() {
		mixer?.update(clock.getDelta());
		if ($model?.rotation) {
			$model.rotation.y += 0.01; // Rotation directe
		}
		requestAnimationFrame(animate);
	}

	function handleClick() {
		navigate('/about/scene');
	}

	function createTextMesh(
		text: string,
		position: [number, number, number],
		size: number,
		color: string
	) {
		if (!font) {
			console.error("La police n'est pas encore chargée."); // Ajoutez un message d'erreur
			return null; // Retournez null si la police n'est pas chargée
		}

		const geometry = new TextGeometry(text, {
			font: font,
			size: size,
			height: 0.01 // Épaisseur du texte
		});
		const material = new THREE.MeshPhongMaterial({ color: color });
		const textMesh = new THREE.Mesh(geometry, material);
		textMesh.position.set(position[0], position[1], position[2]);
		return textMesh;
	}
</script>

<div class="scene-container">
	<Canvas renderMode="always">
		<T.AmbientLight intensity={0.5} />
		<T.DirectionalLight position={[5, 10, 7.5]} intensity={1} />
		<T.PerspectiveCamera makeDefault position={[0, 1.5, 5]} fov={75}>
			<OrbitControls />
		</T.PerspectiveCamera>

		{#if $model}
			<T is={$model} rotation.y />
			<T is={createTextMesh('Mon texte en 3D avec svelte', [-1, 2, 0], 0.3, '#ffae00')} />
			<T
				is={createTextMesh(
					'Reste plus que mon texte 3D soiT cliquable',
					[0, 1.5, 0],
					0.1,
					'#ffffff'
				)}
			/>
			<T
				is={createTextMesh('By DJONTSO Victorien ', [0, 1.1, 0.5], 0.07, '#660066')}
				rotation={[0, Math.PI / 4, Math.PI / 12]}
			/>
		{/if}
	</Canvas>
</div>

<style>
	.scene-container {
		position: relative;
		width: 100%;
		height: 100vh;
	}
</style>
