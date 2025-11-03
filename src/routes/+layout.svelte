<script>
	import { page } from '$app/stores';
	import Header from './Header.svelte';
	import './../app.css';
	import Toast from '$lib/components/Toast.svelte';
	export let data;
	// params n'est pas utilisé, mais requis par SvelteKit pour la compatibilité
	export let params = {};
</script>

<div class="app">
	<Toast />
	<Header />

	<main>
		{#key $page.url.pathname}
			<slot />
		{/key}
	</main>

	<footer>
		<p>© 2023 - PRESENT</p>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>