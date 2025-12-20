<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { HTML } from '@threlte/extras';
	import Nissan from './models/Nissan.svelte';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let { geometry } = $props();

	// State for position and rotation
	let x = $state(geometry?.position?.x ?? 0);
	let z = $state(geometry?.position?.z ?? 0);
	let rotationY = $state(0);

	const speed = 0.2; // Slightly faster for better feel
	const rotSpeed = 0.05;

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

	// Update key state for touch/mouse
	const setKeyState = (key: keyof typeof keys, value: boolean) => {
		keys[key] = value;
	};

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
					setKeyState(k, true);
				},
				{ passive: false }
			);
			btn.addEventListener(
				'touchend',
				(e) => {
					e.preventDefault();
					setKeyState(k, false);
				},
				{ passive: false }
			);
		});
	});
</script>

<svelte:window on:keydown={handleKeyDown} on:keyup={handleKeyUp} />

<T.Group position={[x, geometry?.position?.y ?? 0, z]} rotation={[0, rotationY, 0]}>
	<Nissan />

	<!-- Virtual Controls Overlay -->
	<HTML portal={portalTarget}>
		<div class="controls-container">
			<div class="dpad">
				<div class="row cent">
					<button
						bind:this={buttons.ArrowUp}
						class="control-btn up"
						class:active={keys.ArrowUp}
						onmousedown={() => setKeyState('ArrowUp', true)}
						onmouseup={() => setKeyState('ArrowUp', false)}
						onmouseleave={() => setKeyState('ArrowUp', false)}
					>
						<span class="icon">▲</span>
					</button>
				</div>
				<div class="row">
					<button
						bind:this={buttons.ArrowLeft}
						class="control-btn left"
						class:active={keys.ArrowLeft}
						onmousedown={() => setKeyState('ArrowLeft', true)}
						onmouseup={() => setKeyState('ArrowLeft', false)}
						onmouseleave={() => setKeyState('ArrowLeft', false)}
					>
						<span class="icon">◀</span>
					</button>
					<button
						bind:this={buttons.ArrowDown}
						class="control-btn down"
						class:active={keys.ArrowDown}
						onmousedown={() => setKeyState('ArrowDown', true)}
						onmouseup={() => setKeyState('ArrowDown', false)}
						onmouseleave={() => setKeyState('ArrowDown', false)}
					>
						<span class="icon">▼</span>
					</button>
					<button
						bind:this={buttons.ArrowRight}
						class="control-btn right"
						class:active={keys.ArrowRight}
						onmousedown={() => setKeyState('ArrowRight', true)}
						onmouseup={() => setKeyState('ArrowRight', false)}
						onmouseleave={() => setKeyState('ArrowRight', false)}
					>
						<span class="icon">▶</span>
					</button>
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

	.dpad {
		display: flex;
		flex-direction: column;
		gap: 10px;
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(10px);
		padding: 20px;
		border-radius: 24px;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
