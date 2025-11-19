<script lang="ts">
	import *as T from '@threlte/core';
	import GltfModel from '$lib/components/GltfModel.svelte';

	export let geometry: any;
</script>

<!-- 
  Logique de rendu simplifiée et corrigée :
  1. Priorité aux modèles GLTF via `model_url`.
  2. Sinon, rendu des formes primitives de base via `type`.
-->

<T.Group
	position={[geometry.position.x, geometry.position.y, geometry.position.z]}
	rotation={[geometry.rotation.x, geometry.rotation.y, geometry.rotation.z]}
	scale={geometry.scale || 1}
>
	{#if geometry.model_url}
		<!-- 1. Affiche un modèle GLTF si model_url est présent -->
		<GltfModel url={geometry.model_url} />

	{:else if geometry.type === 'box'}
		<!-- 2. Affiche les formes primitives -->
		<T.Mesh>
			<T.BoxGeometry />
			<T.MeshStandardMaterial color={geometry.color} />
		</T.Mesh>

	{:else if geometry.type === 'torus'}
		<T.Mesh>
			<T.TorusKnotGeometry args={[0.5, 0.15, 100, 12, 2, 3]} />
			<T.MeshStandardMaterial color={geometry.color} />
		</T.Mesh>

	{:else if geometry.type === 'icosahedron'}
		<T.Mesh>
			<T.IcosahedronGeometry />
			<T.MeshStandardMaterial color={geometry.color} />
		</T.Mesh>

	{:else if geometry.type === 'sphere'}
		<T.Mesh>
			<T.SphereGeometry />
			<T.MeshStandardMaterial color={geometry.color} />
		</T.Mesh>

	{:else}
		<!-- Fallback pour les types inconnus : affiche une boîte violette -->
		<T.Mesh>
			<T.BoxGeometry />
			<T.MeshStandardMaterial color="purple" />
		</T.Mesh>
	{/if}
</T.Group>