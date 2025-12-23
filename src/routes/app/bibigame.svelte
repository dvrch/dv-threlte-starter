<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import Bibi3 from './models/Bibi3.svelte';

	let { geometry } = $props();

	// State for position and rotation (Relative to parent Dynamic3DModel)
	let x = $state(0);
	let z = $state(0);
	let rotationY = $state(0);

	// Physical State
	let speed_current = $state(0);
	const acceleration = 0.005;
	const friction = 0.98;
	const maxSpeed = 0.5;
	const backSpeed = 0.2;
	const turnEase = 0.9;
	const rotSpeed = 0.03;
	let currentRotationSpeed = $state(0);

	// Keyboard/Touch state
	let keys = $state({
		ArrowUp: false,
		ArrowDown: false,
		ArrowLeft: false,
		ArrowRight: false
	});

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key in keys) keys[e.key as keyof typeof keys] = true;
	}

	function handleKeyUp(e: KeyboardEvent) {
		if (e.key in keys) keys[e.key as keyof typeof keys] = false;
	}

	// Game loop
	useTask(() => {
		if (keys.ArrowUp) {
			speed_current += acceleration;
		} else if (keys.ArrowDown) {
			speed_current -= acceleration;
		} else {
			speed_current *= friction;
		}

		if (speed_current > maxSpeed) speed_current = maxSpeed;
		if (speed_current < -backSpeed) speed_current = -backSpeed;

		if (keys.ArrowLeft) {
			currentRotationSpeed += rotSpeed * 0.25;
		} else if (keys.ArrowRight) {
			currentRotationSpeed -= rotSpeed * 0.25;
		} else {
			currentRotationSpeed *= turnEase;
		}

		if (currentRotationSpeed > rotSpeed) currentRotationSpeed = rotSpeed;
		if (currentRotationSpeed < -rotSpeed) currentRotationSpeed = -rotSpeed;

		const turningFactor = Math.abs(speed_current) > 0.05 ? (speed_current > 0 ? 1 : -1) : 0;
		rotationY += currentRotationSpeed * turningFactor * (Math.abs(speed_current) / maxSpeed + 0.5);

		x += Math.sin(rotationY) * speed_current;
		z += Math.cos(rotationY) * speed_current;
	});
</script>

<svelte:window on:keydown={handleKeyDown} on:keyup={handleKeyUp} />

<T.Group position={[x, 0, z]} rotation={[0, rotationY, 0]}>
	<Bibi3 />
</T.Group>

