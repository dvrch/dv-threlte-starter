<script>
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import { services } from './index';

	

	let isInView = $state(false);

	onMount(() => {
		const observer = new IntersectionObserver(
			([entry]) => {
				isInView = entry.isIntersecting;
			},
			{ threshold: 0.5 }
		);

		const element = document.querySelector('#about');
		if (element) observer.observe(element);

		return () => observer.disconnect();
	});
</script>

<section id="about" class="relative w-full mx-auto">
	{#if isInView}
		<div in:fade={{ duration: 1000 }} class="max-w-7xl mx-auto sm:px-16 px-6 sm:py-16 py-10">
			<div class="mt-4 text-secondary text-[17px] max-w-3xl leading-[30px]">
				<!-- Contenu About -->
			</div>

			<div class="mt-20 flex flex-wrap gap-10">
				{#each services as service}
					<div class="xs:w-[250px] w-full" in:fade={{ duration: 1000, delay: 500 }}>
						<div class="w-full green-pink-gradient p-[1px] rounded-[20px] shadow-card">
							<div
								class="bg-tertiary rounded-[20px] py-5 px-12 min-h-[280px] flex justify-evenly items-center flex-col"
							>
								<img src={service.icon} alt={service.title} class="w-16 h-16 object-contain" />
								=
								<h3 class="text-white text-[20px] font-bold text-center">{service.title}</h3>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</section>
