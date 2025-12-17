<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import Nissan from './models/Nissan.svelte'; // Assuming relative import or use $lib
	import { writable } from 'svelte/store';

	let { geometry } = $props();

	// State for position and rotation
	let x = $state(geometry?.position?.x ?? 0);
	let z = $state(geometry?.position?.z ?? 0);
	let rotationY = $state(0);

	const speed = 0.1;
	const rotSpeed = 0.05;

	// Keyboard state
	let keys = {
		ArrowUp: false,
		ArrowDown: false,
		ArrowLeft: false,
		ArrowRight: false
	};

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key in keys) keys[e.key as keyof typeof keys] = true;
	}

	function handleKeyUp(e: KeyboardEvent) {
		if (e.key in keys) keys[e.key as keyof typeof keys] = false;
	}

	// Game loop
	useTask(() => {
		if (keys.ArrowUp) {
			x += Math.sin(rotationY) * speed;
			z += Math.cos(rotationY) * speed;
		}
		if (keys.ArrowDown) {
			x -= Math.sin(rotationY) * speed;
			z -= Math.cos(rotationY) * speed;
		}
		if (keys.ArrowLeft) {
			rotationY += rotSpeed;
		}
		if (keys.ArrowRight) {
			rotationY -= rotSpeed;
		}
	});
</script>

<svelte:window on:keydown={handleKeyDown} on:keyup={handleKeyUp} />

<T.Group position={[x, geometry?.position?.y ?? 0, z]} rotation={[0, rotationY, 0]}>
	<Nissan />
</T.Group>
