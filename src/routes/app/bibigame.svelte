<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { HTML, OrbitControls } from '@threlte/extras';
	import Bibi3 from './models/Bibi3.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

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
			mouseXPercentage = (e.clientX / window.innerWidth) * 2 - 1;

			mouseMoving = true;
			if (mouseMoveTimeout) clearTimeout(mouseMoveTimeout);
			mouseMoveTimeout = setTimeout(() => {
				mouseMoving = false;
			}, 100);
		}
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
		} else if (mouseMoving && (keys.ArrowUp || keys.ArrowDown)) {
			currentRotationSpeed -= mouseXPercentage * rotSpeed * 0.5;
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

<T.Group position={[x, 0, z]} rotation={[0, rotationY, 0]}>
	<Bibi3 />

	{#if isChaseCamActive}
		<T.PerspectiveCamera
			makeDefault
			position={[0, 4, -8]}
			fov={60}
			on:create={({ ref }) => {
				ref.lookAt(0, 1, 5);
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
		background: rgba(0, 0, 0, 0.1); /* More transparent background */
		backdrop-filter: blur(4px); /* Slightly less blur */
		padding: 10px 15px;
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.05); /* More transparent border */
		color: white;
		font-family: 'Orbitron', sans-serif;
		transform: scale(0.8);
		transform-origin: top left;
		transition: all 0.3s ease;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2); /* Softer shadow */
	}

	.speed-gauge .value {
		font-size: 2.2rem;
		font-weight: bold;
		color: #ff6e40;
		text-shadow: 0 0 10px rgba(255, 110, 64, 0.4); /* Softer text shadow */
	}

	.dpad {
		display: flex;
		flex-direction: column;
		gap: 8px;
		background: rgba(0, 0, 0, 0.2); /* More transparent background */
		backdrop-filter: blur(6px); /* Slightly less blur */
		padding: 12px;
		border-radius: 20px;
		border: 1px solid rgba(255, 255, 255, 0.05); /* More transparent border */
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); /* Softer shadow */
	}

	.row {
		display: flex;
		gap: 12px;
		justify-content: center;
	}

	.control-btn {
		width: 65px;
		height: 65px;
		border: none;
		border-radius: 18px;
		background: rgba(255, 255, 255, 0.05); /* More transparent background */
		color: rgba(255, 255, 255, 0.6); /* More transparent text color */
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.2s;
		font-size: 26px;
		border: 1px solid rgba(255, 255, 255, 0.02); /* More transparent border */
	}

	.control-btn:active,
	.control-btn.active {
		background: rgba(255, 110, 64, 0.2); /* Softer active background */
		box-shadow: 0 0 15px rgba(255, 110, 64, 0.2); /* Softer active shadow */
		transform: scale(0.95);
		border-color: rgba(255, 110, 64, 0.3); /* Softer active border */
	}

	@media (max-width: 768px) {
		.control-btn {
			width: 80px;
			height: 80px;
		}
	}
</style>
