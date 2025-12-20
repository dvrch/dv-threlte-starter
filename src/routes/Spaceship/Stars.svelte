<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { Instance, InstancedMesh, useTexture } from '@threlte/extras';
	import { Color, DoubleSide, Vector3 } from 'three';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';

	let STARS_COUNT = 350;
	let colors = ['#fcaa67', '#C75D59', '#ffffc7', '#8CC5C6', '#A5898C'];

	interface Star {
		pos: Vector3;
		len: number;
		speed: number;
		color: Color;
		rad: number;
	}

	let stars = $state<Star[]>([]);
	let starUrl = $state('');

	const map = useTexture(() => starUrl || '');

	onMount(async () => {
		if (browser) {
			starUrl = await getWorkingAssetUrl('star.png', 'textures');
		}
	});

	function r(min: number, max: number) {
		return min + Math.random() * (max - min);
	}

	function createStar(): Star {
		let pos: Vector3;
		let len: number;

		if (Math.random() > 0.8) {
			pos = new Vector3(r(-10, -30), r(-5, 5), r(6, -6));
			len = r(1.5, 15);
		} else {
			pos = new Vector3(r(-15, -45), r(-10.5, 1.5), r(30, -45));
			len = r(2.5, 20);
		}

		return {
			pos,
			len,
			speed: r(19.5, 42),
			rad: r(0.04, 0.07),
			color: new Color(colors[Math.floor(Math.random() * colors.length)])
				.convertSRGBToLinear()
				.multiplyScalar(1.3)
		};
	}

	for (let i = 0; i < STARS_COUNT; i++) {
		stars.push(createStar());
	}

	useTask((delta) => {
		for (let i = 0; i < stars.length; i++) {
			const star = stars[i];
			star.pos.x += star.speed * delta;
			if (star.pos.x > 40) {
				const newStar = createStar();
				stars[i].pos.copy(newStar.pos);
				stars[i].speed = newStar.speed;
				stars[i].len = newStar.len;
				stars[i].color.copy(newStar.color);
			}
		}
	});
</script>

{#if $map}
	<InstancedMesh limit={STARS_COUNT} range={STARS_COUNT}>
		<T.PlaneGeometry args={[1, 0.05]} />
		<T.MeshBasicMaterial side={DoubleSide} alphaMap={$map} transparent />

		{#each stars as star}
			<Instance
				position={[star.pos.x, star.pos.y, star.pos.z]}
				scale={[star.len, 1, 1]}
				color={star.color}
			/>
		{/each}
	</InstancedMesh>
{/if}
