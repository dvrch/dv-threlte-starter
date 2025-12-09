<script lang="ts">
	import { Canvas, T } from '@threlte/core'
	import Earth from './Earth.svelte'
	import { onMount } from 'svelte'
	import * as THREE from 'three'

	let { data } = $props();
</script>

<Canvas renderMode="always">
	<Earth />
</Canvas>

