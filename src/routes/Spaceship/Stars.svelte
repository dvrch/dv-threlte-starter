<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { Instance, InstancedMesh } from '@threlte/extras';
	import { Color, DoubleSide, Vector3, TextureLoader } from 'three';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { getWorkingAssetUrl } from '$lib/utils/assetFallback';

	let STARS_COUNT = 1200;
	let colors = ['#fcaa67', '#C75D59', '#ffffc7', '#8CC5C6', '#A5898C'];

	interface Star {
		pos: Vector3;
		len: number;
		speed: number;
		color: Color;
		rad: number;
	}

	let stars = $state<Star[]>([]);
	let texture = $state<any>(null);

	onMount(async () => {
		if (browser) {
			const url = await getWorkingAssetUrl('star.png', 'textures');
			const loader = new TextureLoader();
			texture = await loader.loadAsync(url);
		}
	});

	function r(min: number, max: number) {
		return min + Math.random() * (max - min);
	}

	function createStar(): Star {
		let pos: Vector3;
		let len: number;

		// Massively expanded star field tunnel
		pos = new Vector3(r(-250, 50), r(-150, 150), r(-150, 150));
		len = r(2, 35);

		return {
			pos,
			len,
			speed: r(20, 60),
			rad: r(0.04, 0.1),
			color: new Color(colors[Math.floor(Math.random() * colors.length)])
				.convertSRGBToLinear()
				.multiplyScalar(1.8)
		};
	}

	for (let i = 0; i < STARS_COUNT; i++) {
		stars.push(createStar());
	}

	useTask((delta) => {
		for (let i = 0; i < stars.length; i++) {
			const star = stars[i];
			star.pos.x += star.speed * delta;
			if (star.pos.x > 150) {
				const newStar = createStar();
				stars[i].pos.copy(newStar.pos);
				stars[i].speed = newStar.speed;
				stars[i].len = newStar.len;
				stars[i].color.copy(newStar.color);
			}
		}
	});
</script>

{#if texture}
	<InstancedMesh limit={STARS_COUNT} range={STARS_COUNT} name="Starfield">
		<T.PlaneGeometry args={[1, 0.05]} />
		<T.MeshBasicMaterial side={DoubleSide} alphaMap={texture} transparent />

		{#each stars as star}
			<Instance
				position={[star.pos.x, star.pos.y, star.pos.z]}
				scale={[star.len, 1, 1]}
				color={star.color}
			/>
		{/each}
	</InstancedMesh>
{/if}
