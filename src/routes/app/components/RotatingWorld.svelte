<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { browser } from '$app/environment';

	let rotationY = $state(0);
	const { children } = $props();

	useTask((delta) => {
		rotationY += 0.2 * delta; // Slow rotation
	});
</script>

<T.Group rotation.y={rotationY}>
	{@render children()}
</T.Group>
