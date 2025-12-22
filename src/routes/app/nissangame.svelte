<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { HTML, OrbitControls } from '@threlte/extras';
	import Nissan from './models/Nissan.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let { geometry } = $props();

	// State for position and rotation (Relative to parent Dynamic3DModel)
	let x = $state(0);
	let z = $state(0);
	let rotationY = $state(0);

	// Physical State
	let speed_current = $state(0);
	const acceleration = 0.005; // Reduced by half
	const friction = 0.98; // Smoother friction
	const maxSpeed = 0.5; // Slightly slower for more control
	const backSpeed = 0.2;
	const turnEase = 0.9;
	const rotSpeed = 0.03; // Slightly slower rotation for precision
	let currentRotationSpeed = $state(0);
	let isChaseCamActive = $state(false);
	let mouseXPercentage = $state(0);
	let mouseMoving = $state(false);
	let mouseMoveTimeout: any;

	// Keyboard/Touch state
	let keys = $state({
		ArrowUp: false,
		ArrowDown: false,
		ArrowLeft: false,
		ArrowRight: false
	});

	let portalTarget = $state<HTMLElement | undefined>(undefined);
	$effect(() => {
		portalTarget = document.body;
	});

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key in keys) keys[e.key as keyof typeof keys] = true;
	}

	function handleKeyUp(e: KeyboardEvent) {
		if (e.key in keys) keys[e.key as keyof typeof keys] = false;
	}

	function handlePointerMove(e: PointerEvent) {
		if (browser) {
			// Calculate normalized mouse X position (-1 to 1)
			mouseXPercentage = (e.clientX / window.innerWidth) * 2 - 1;

			// Track mouse activity
			mouseMoving = true;
			if (mouseMoveTimeout) clearTimeout(mouseMoveTimeout);
			mouseMoveTimeout = setTimeout(() => {
				mouseMoving = false;
			}, 100);
		}
	}

	// Game loop
	useTask(() => {
		// Movement logic
		if (keys.ArrowUp) {
			speed_current += acceleration;
		} else if (keys.ArrowDown) {
			speed_current -= acceleration;
		} else {
			speed_current *= friction;
		}

		// Clamp speed
		if (speed_current > maxSpeed) speed_current = maxSpeed;
		if (speed_current < -backSpeed) speed_current = -backSpeed;

		// Steering
		if (keys.ArrowLeft) {
			currentRotationSpeed += rotSpeed * 0.25;
		} else if (keys.ArrowRight) {
			currentRotationSpeed -= rotSpeed * 0.25;
		} else if (mouseMoving && (keys.ArrowUp || keys.ArrowDown)) {
			// Mouse steering ONLY when moving mouse and accelerating/braking
			currentRotationSpeed -= mouseXPercentage * rotSpeed * 0.5;
		} else {
			currentRotationSpeed *= turnEase;
		}

		// Clamp rotation speed
		if (currentRotationSpeed > rotSpeed) currentRotationSpeed = rotSpeed;
		if (currentRotationSpeed < -rotSpeed) currentRotationSpeed = -rotSpeed;

		// Apply movement: Only rotate if moving significantly
		const turningFactor = Math.abs(speed_current) > 0.05 ? (speed_current > 0 ? 1 : -1) : 0;

		rotationY += currentRotationSpeed * turningFactor * (Math.abs(speed_current) / maxSpeed + 0.5);

		x += Math.sin(rotationY) * speed_current;
		z += Math.cos(rotationY) * speed_current;
	});

	// Handle touch events non-passively to stop scrolling
	let buttons: Record<string, HTMLButtonElement> = {};
	onMount(() => {
		Object.entries(buttons).forEach(([key, btn]) => {
			if (!btn) return;
			const k = key as keyof typeof keys;
			btn.addEventListener(
				'touchstart',
				(e) => {
					e.preventDefault();
					keys[k] = true;
				},
				{ passive: false }
			);
			btn.addEventListener(
				'touchend',
				(e) => {
					e.preventDefault();
					keys[k] = false;
				},
				{ passive: false }
			);
		});
	});
</script>

<svelte:window
	on:keydown={handleKeyDown}
	on:keyup={handleKeyUp}
	on:pointermove={handlePointerMove}
/>

<T.Group position={[x, 0, z]} rotation={[0, rotationY, 0]} on:create={() => {}}>
	<Nissan />

	<!-- Chase Camera (Only active if toggled) -->
	{#if isChaseCamActive}
		<T.PerspectiveCamera
			makeDefault
			position={[0, 4, -8]}
			fov={60}
			on:create={({ ref }) => {
				ref.lookAt(0, 1, 5); // Look slightly ahead of the car
			}}
		>
			<OrbitControls
				enableDamping
				autoRotate={!isChaseCamActive}
				autoRotateSpeed={0.5}
				target={[0, 1, 2]}
			/>
		</T.PerspectiveCamera>
	{/if}

	<!-- Virtual Controls Overlay -->
	<HTML portal={portalTarget}>
		<div class="game-ui">
			<div class="dashboard">
				<div class="speed-gauge">
					<span class="value">{Math.abs(Math.round(speed_current * 1000))}</span>
					<span class="unit">KM/H</span>
				</div>
				<button
					class="cam-toggle"
					class:active={isChaseCamActive}
					onclick={() => (isChaseCamActive = !isChaseCamActive)}
				>
					{isChaseCamActive ? 'CAM: CHASE' : 'CAM: EDITOR'}
				</button>
			</div>

			<div class="controls-container">
				<div class="dpad">
					<div class="row cent">
						<button
							bind:this={buttons.ArrowUp}
							class="control-btn up"
							class:active={keys.ArrowUp}
							onmousedown={() => (keys.ArrowUp = true)}
							onmouseup={() => (keys.ArrowUp = false)}
							onmouseleave={() => (keys.ArrowUp = false)}
						>
							<span class="icon">▲</span>
						</button>
					</div>
					<div class="row">
						<button
							bind:this={buttons.ArrowLeft}
							class="control-btn left"
							class:active={keys.ArrowLeft}
							onmousedown={() => (keys.ArrowLeft = true)}
							onmouseup={() => (keys.ArrowLeft = false)}
							onmouseleave={() => (keys.ArrowLeft = false)}
						>
							<span class="icon">◀</span>
						</button>
						<button
							bind:this={buttons.ArrowDown}
							class="control-btn down"
							class:active={keys.ArrowDown}
							onmousedown={() => (keys.ArrowDown = true)}
							onmouseup={() => (keys.ArrowDown = false)}
							onmouseleave={() => (keys.ArrowDown = false)}
						>
							<span class="icon">▼</span>
						</button>
						<button
							bind:this={buttons.ArrowRight}
							class="control-btn right"
							class:active={keys.ArrowRight}
							onmousedown={() => (keys.ArrowRight = true)}
							onmouseup={() => (keys.ArrowRight = false)}
							onmouseleave={() => (keys.ArrowRight = false)}
						>
							<span class="icon">▶</span>
						</button>
					</div>
				</div>
			</div>
		</div>
	</HTML>
</T.Group>

<style>
	.controls-container {
		position: fixed;
		bottom: 40px;
		right: 40px;
		user-select: none;
		pointer-events: auto;
		z-index: 1000;
	}

	.game-ui {
		position: fixed;
		inset: 0;
		pointer-events: none;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		padding: 40px;
	}

	.dashboard {
		align-self: flex-start;
		background: rgba(0, 0, 0, 0.1);
		backdrop-filter: blur(2px);
		padding: 8px 12px;
		border-radius: 10px;
		border: 1px solid rgba(255, 255, 255, 0.03);
		color: rgba(255, 255, 255, 0.3);
		font-family: 'Orbitron', sans-serif;
		transform: scale(0.7);
		transform-origin: top left;
		transition: all 0.4s ease;
		opacity: 0.15;
	}

	.dashboard:hover {
		opacity: 0.8;
		background: rgba(0, 0, 0, 0.3);
		color: white;
	}

	.speed-gauge {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.speed-gauge .value {
		font-size: 2rem;
		font-weight: bold;
		color: #4287f5;
		text-shadow: 0 0 10px rgba(66, 135, 245, 0.5);
	}

	.speed-gauge .unit {
		font-size: 0.7rem;
		opacity: 0.7;
		letter-spacing: 2px;
		margin-bottom: 10px;
	}

	.cam-toggle {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: white;
		padding: 5px 10px;
		border-radius: 8px;
		font-size: 0.6rem;
		cursor: pointer;
		pointer-events: auto;
		transition: all 0.2s;
		width: 100%;
	}

	.cam-toggle:hover {
		background: rgba(255, 255, 255, 0.2);
	}

	.cam-toggle.active {
		background: #4287f5;
		border-color: #4287f5;
		box-shadow: 0 0 10px rgba(66, 135, 245, 0.5);
	}

	.dpad {
		display: flex;
		flex-direction: column;
		gap: 6px;
		background: rgba(255, 255, 255, 0.01);
		backdrop-filter: blur(2px);
		padding: 8px;
		border-radius: 16px;
		border: 1px solid rgba(255, 255, 255, 0.01);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		opacity: 0.1;
		transition: all 0.4s ease;
		transform: scale(0.8);
	}

	.dpad:hover {
		opacity: 0.6;
		background: rgba(255, 255, 255, 0.05);
	}

	.row {
		display: flex;
		gap: 10px;
		justify-content: center;
	}

	.control-btn {
		width: 60px;
		height: 60px;
		border: none;
		border-radius: 16px;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
		font-size: 24px;
		border: 1px solid rgba(255, 255, 255, 0.05);
	}

	.control-btn:hover {
		background: rgba(255, 255, 255, 0.2);
		transform: scale(1.05);
	}

	.control-btn:active,
	.control-btn.active {
		background: rgba(66, 135, 245, 0.4);
		box-shadow: 0 0 20px rgba(66, 135, 245, 0.3);
		transform: scale(0.95);
		border-color: rgba(66, 135, 245, 0.5);
	}

	.icon {
		display: flex;
		align-items: center;
		justify-content: center;
		filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.3));
	}

	/* Optional: adjustments for touch devices */
	@media (max-width: 768px) {
		.control-btn {
			width: 70px;
			height: 70px;
			font-size: 28px;
		}
		.controls-container {
			bottom: 20px;
			right: 20px;
		}
	}
</style>
