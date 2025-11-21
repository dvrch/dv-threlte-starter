<script lang="ts">
	import { Canvas, T } from '@threlte/core'
	import Earth from './Earth.svelte'
	import { onMount } from 'svelte'
	import * as THREE from 'three'

	export const data = undefined;
</script>

<Canvas>
	<Earth />
</Canvas>

