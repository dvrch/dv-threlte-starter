<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { browser } from '$app/environment';

	let { children, isPaused = false } = $props();
	let rotationY = $state(0);

	useTask((delta) => {
		if (isPaused) return;
		rotationY += 0.2 * delta; // Slow rotation
	});
</script>

<T.Group rotation.y={rotationY}>
	{@render children()}
</T.Group>
