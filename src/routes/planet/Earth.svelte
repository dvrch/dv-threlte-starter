<script lang="ts">
	import { T } from '@threlte/core';
	import { useGltf } from '@threlte/extras';
	import { dracoLoader } from '$lib/utils/draco';

	import { assets } from '$lib/services/assets';

	// Charger le modèle GLTF.
	// Le hook useGltf est appelé au niveau supérieur du script.
	// Le chemin '/models/scene.gltf' pointe vers le dossier 'static/models/scene.gltf'.
	const gltf = useGltf(assets.getUrl('/models/scene.gltf'), { dracoLoader });
</script>

<!--
  Le résultat de useGltf est un "store" Svelte.
  On peut y accéder directement dans le template avec la syntaxe `$gltf`.
  Threlte attend que le store soit résolu avant de tenter le rendu.
  La propriété `scene` de l'objet GLTF est ce que nous voulons afficher.
-->
{#if $gltf}
	<T is={$gltf.scene} />
{/if}
